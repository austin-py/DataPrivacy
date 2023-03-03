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

dp = DataProcecssor()

model = ols("""Response ~ C(IntrovertExtrovert) + C(AdMatchedUnmatched) + C(TargetedUntargeted)
            + C(IntrovertExtrovert):C(AdMatchedUnmatched) + C(IntrovertExtrovert):C(TargetedUntargeted) + C(AdMatchedUnmatched):C(TargetedUntargeted)
            + C(IntrovertExtrovert):C(AdMatchedUnmatched):C(TargetedUntargeted)""", data = dp.data).fit()

results = sm.stats.anova_lm(model, typ=2)

# print(results)

"""
Austin's brief interpretation: 

Since P < 0.05 for AdMatchedUnmatched this likely had a significant effect 

Since P ~ 0.07 for Introvert Extrovert this indicates some effect, but might not reach signfigance 

P ~ 0.18 for Targeted Untargeted so this didn't seem to have a huge effect 

"""




test = __convert_freqs_to_list_of_nums__(dp,dp.extrovert_counts)
test2 = __convert_freqs_to_list_of_nums__(dp, dp.introvert_counts)

f, p = f_oneway(test,test2)
# print(f,p)

"""
P value is significance 
"""









