import os
import pandas as pd
import numpy as np

if __name__ == '__main__':

    # files = os.listdir('data')
    post_data = pd.read_csv('data/karma_post_responses.csv', sep=';')
    order = pd.read_csv('data/karma_order.csv', sep=';')
    objective_data = pd.read_csv('data/karma_objective.csv', sep='\t')

    # Remap post
    qs = [
        'leuk',
        'vriendelijk',
        'aardig',
        'aangenaam',
        'fijn',
        'vertrouwen',
        'sympathie',
        'graag',
        'band',
        'gemoed',
        'responsief',
        'invloed',
        'opmerken',
        'bewust',
        'niet_alleen',
    ]
    new_cols = ['pp', 'couple', 'partner']
    for i in range(1, 4):
        new_cols += [f'cond{i}_{q}' for q in qs]
    new_cols += ['nieuwe_wereld', 'reis', 'vergeten', 'bezoek']
    post_data.columns = new_cols
    post_data.sort_values(by=['pp', 'couple', 'partner'], inplace=True)

    # Remap order
    order.insert(0, 'couple', list(range(1, 19)))
    order.drop(columns=['volgorde'], inplace=True)
    order.columns = [
        'couple',
        'cond1_scen',
        'cond2_scen',
        'cond3_scen',
        'cond1_role1',
        'cond2_role1',
        'cond3_role1',
        '_cham1',
        '_cham2',
        '_cham3',
        'cond1_chameleon',
        'cond2_chameleon',
        'cond3_chameleon',
    ]

    # Who's talking to a chameleon?
    for cond in [1, 2, 3]:
        for partner in [1, 2]:
            order[f'cond{cond}_partner{partner}_chameleon'] = order[
                f'cond{cond}_chameleon'
            ].apply(lambda x: 1 if (x == ((partner%2)+1)) else 0)

    order_partner1 = order[
        [
            c
            for c in list(order.columns)
            if c.__contains__('partner1') or c == 'couple'
        ]
    ]
    order_partner2 = order[
        [
            c
            for c in list(order.columns)
            if c.__contains__('partner2') or c == 'couple'
        ]
    ]
    order_partner1.insert(0, 'partner', 1)
    order_partner2.insert(0, 'partner', 2)
    order_partner1.columns = [
        'partner',
        'couple',
        'cond1_chameleon',
        'cond2_chameleon',
        'cond3_chameleon',
    ]
    order_partner2.columns = [
        'partner',
        'couple',
        'cond1_chameleon',
        'cond2_chameleon',
        'cond3_chameleon',
    ]
    order_long = pd.concat([order_partner1, order_partner2])

    # Combine data
    combined = pd.merge(left=post_data, right=order_long, on=['couple', 'partner'])

    # To long format
    dfs = []
    for c in range(1,4):
        sub_df = combined[['pp', 'couple', 'partner'] + [col for col in combined.columns if col.startswith(f'cond{c}')]]
        sub_df.columns = ['pp','couple','partner'] + qs + ['chameleon']
        sub_df.insert(3, 'condition', c)
        dfs.append(sub_df)
    long_df = pd.concat(dfs)

    # Combine scores
    long_df['positive_perception'] = long_df.leuk + long_df.vriendelijk + long_df.aardig + long_df.aangenaam + long_df.fijn
    long_df['bond'] = long_df.vertrouwen + long_df.gemoed + long_df.sympathie + long_df.graag
    long_df['copresence'] = long_df.responsief + long_df.invloed + long_df.opmerken + long_df.bewust + long_df.niet_alleen

    long_df.to_csv('data/long.csv', index=False, sep=';')

