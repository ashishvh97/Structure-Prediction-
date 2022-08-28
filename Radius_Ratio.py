import smact
import pandas as pd
from pymatgen.ext.matproj import MPRester
from pymatgen.core import Composition
from pymatgen.analysis.local_env import CrystalNN

m = MPRester("zGaTtrIMhHdZD1Fo")  # use API key generated from Materials Project Dashboard


# function to return cationic oxidation state
def cat_os(x):
    comp = Composition(x)
    os = comp.oxi_state_guesses()
    if len(os) > 0:
        oxidation_states = list(os[0].values())
    else:
        oxidation_states = [0, 0]

    return oxidation_states[0]


# function to return anion's oxidation state

def an_os(x):
    comp = Composition(x)
    os = comp.oxi_state_guesses()
    if len(os) > 0:
        oxidation_states = list(os[0].values())
    else:
        oxidation_states = [0, 0]

    return oxidation_states[1]


# query for binary 1:1 materials with icsd ids
anon_formula = {'A': 1, 'B': 1}
binary = m.query(criteria={'anonymous_formula': anon_formula, 'icsd_ids': {'$gte': 0}},
                 properties=['pretty_formula', 'material_id', 'spacegroup.symbol', 'spacegroup.crystal_system',
                             'icsd_ids', 'e_above_hull', 'final_energy', 'density'])

binary_df = pd.DataFrame(binary)
df = binary_df.sort_values(['pretty_formula', 'e_above_hull'])
df = df.reset_index(drop=True)
df = df.drop_duplicates('pretty_formula', keep='first')

df = df.reset_index(drop=True)

df['cation_oxidation_state'] = df['pretty_formula'].apply(cat_os)
df['anion_oxidation_state'] = df['pretty_formula'].apply(an_os)

# dropping the compositions with no oxidation states (cation_oxidation_state = 0)
df = df[df.cation_oxidation_state != 0]


# using local_env to guess coordination numbers

def co_ordination_num(y):
    structure = m.get_structure_by_material_id(y)
    crystal = CrystalNN()
    cn = crystal.get_cn(structure, 0)
    return cn


df['coordination_number'] = df['material_id'].apply(co_ordination_num)

# create a new dataframe for radius ratio rules
df_new = df.copy()


# function to return radius ratio and corresponding coordination number and geometry
def radius_ratio(x):
    comp = Composition(x.pretty_formula)
    elements = comp.chemical_system
    # split the individual elements in the system
    i_element = elements.partition('-')

    # create cation and anion species using smact
    cat = smact.Species(i_element[0], x.cation_oxidation_state)
    an = smact.Species(i_element[2], x.anion_oxidation_state)

    # calculate radius ratio
    rad_ratio = cat.average_ionic_radius / an.average_ionic_radius

    return rad_ratio


df_new['radius_ratio'] = df_new.apply(radius_ratio, axis=1)

# drop NaN radius ratios
df_new_2 = df_new.dropna().reset_index(drop=True)


# function to predict coordination number from radius ratios
def rr_predict_cn(x):
    if x.radius_ratio <= 0.155:
        return [2]
    elif 0.155 < x.radius_ratio <= 0.225:
        return [3]
    elif 0.225 < x.radius_ratio <= 0.414:
        return [4]
    elif 0.414 < x.radius_ratio <= 0.732:
        return [4, 6]
    elif 0.732 < x.radius_ratio <= 1.0:
        return [8]
    else:
        return [12]


df_new_2['predicted_coordination_numbers'] = df_new_2.apply(rr_predict_cn, axis=1)


# function to compare the predicted and true coordination numbers
def comparison(x):
    if x.coordination_number in x.predicted_coordination_numbers:
        return 'correct'
    else:
        return 'incorrect'


df_new_2['Comparison'] = df_new_2.apply(comparison, axis=1)
print(df_new_2['Comparison'].value_counts())

ax = df_new_2['Comparison'].value_counts().plot(kind='bar', figsize=(16, 9), color='steelblue')
ax.set_xlabel('Validation')
ax.set_ylabel('Counts')
