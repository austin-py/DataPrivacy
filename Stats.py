import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import f_oneway

from Classes.DataProcessor import DataProcecssor

def __convert_freqs_to_list_of_nums__(dp,lst):
    result = []
    for key in dp.response_to_num.keys():
        if key in lst:
            num = lst[key]
            for i in range(num):
                result.append(dp.response_to_num[key])
    return result 

#ANOVA 

dp = DataProcecssor()

model = ols("""Response ~ C(IntrovertExtrovert) + C(AdMatchedUnmatched) + C(TargetedUntargeted)
            + C(IntrovertExtrovert):C(AdMatchedUnmatched) + C(IntrovertExtrovert):C(TargetedUntargeted) + C(AdMatchedUnmatched):C(TargetedUntargeted)
            + C(IntrovertExtrovert):C(AdMatchedUnmatched):C(TargetedUntargeted)""", data = dp.data).fit()

anova_results = sm.stats.anova_lm(model, typ=2)

# print(results)

"""
Austin's brief interpretation: 

Since P < 0.05 for AdMatchedUnmatched this likely had a significant effect 

Since P ~ 0.07 for Introvert Extrovert this indicates some effect, but might not reach signfigance 

P ~ 0.18 for Targeted Untargeted so this didn't seem to have a huge effect 

"""

#T-Tests
dicts = [dp.extrovert_counts,
         dp.introvert_counts,
         dp.introvert_who_got_introvert_counts,
         dp.extrovert_who_got_extrovert_counts,
         dp.introverts_who_got_extrovert_counts,
         dp.extrovert_who_got_introvert_counts,
         dp.introverts_who_got_introvert_ad_untargeted_counts,
         dp.introverts_who_got_extrovert_ad_untargeted_counts,
         dp.introverts_who_got_introvert_ad_targeted_counts,
         dp.introverts_who_got_extrovert_ad_targeted_counts,
         dp.extroverts_who_got_introvert_ad_untargeted_counts,
         dp.extroverts_who_got_extrovert_ad_untargeted_counts,
         dp.extroverts_who_got_introvert_ad_targeted_counts,
         dp.extroverts_who_got_extrovert_ad_targeted_counts,
         #TODO add any other dictionaries we add here 
         ]
t_test_results = {}

for d1 in dicts:
    for d2 in dicts:
        vals_d1 = __convert_freqs_to_list_of_nums__(dp,d1)
        vals_d2 = __convert_freqs_to_list_of_nums__(dp,d2)
        f, p = f_oneway(vals_d1,vals_d2)
        test_name = d1['Name'] + ' vs. ' + d2['Name']
        t_test_results[test_name] = {'f': f, 'p': p}



#Uncomment below to print the tests that met at 0.05 significance level: 


# for i in t_test_results.keys():
    # if t_test_results[i]['p'] <= 0.05:
        # print(i, '     ', t_test_results[i])








