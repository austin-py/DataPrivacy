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
         dp.extroverts_who_got_targeted_counts,
         dp.extroverts_who_got_untargeted_counts,
         dp.introverts_who_got_targeted_counts,
         dp.introverts_who_got_untargeted_counts,
         dp.targeted_counts,
         dp.untargeted_counts,
         dp.matched_untargeted_counts,
         dp.matched_targeted_counts,
         dp.unmatched_untargeted_counts,
         dp.unmatched_targeted_counts,
         dp.matched_counts,
         dp.unmatched_counts]

t_test_results = {}

for d1 in dicts:
    for d2 in dicts:
        vals_d1 = __convert_freqs_to_list_of_nums__(dp,d1)
        vals_d2 = __convert_freqs_to_list_of_nums__(dp,d2)
        f, p = f_oneway(vals_d1,vals_d2)
        test_name = d1['Name'] + ' vs. ' + d2['Name']
        t_test_results[test_name] = {'f': f, 'p': p}

# print(t_test_results)
final_results = {}
# Whether or not the ad is matched to self-perception is significant 
# Whether or not the ad is targeted has less of a difference

# Was there significance between extroverts who were matched vs. extroverts who were unmatched? 
final_results["ExtrovertsWhoGotExtrovertAd vs. ExtrovertsWhoGotIntrovertAd"] = t_test_results["ExtrovertsWhoGotExtrovertAd vs. ExtrovertsWhoGotIntrovertAd"]
# Was there significance between introverts who were matched vs. introverts who were unmatched? 
final_results["IntrovertsWhoGotExtrovertAd vs. IntrovertsWhoGotIntrovertAd"] = t_test_results["IntrovertsWhoGotExtrovertAd vs. IntrovertsWhoGotIntrovertAd"]
# Was there signficiance between general people who were matched vs. unmatched?
final_results["UnMatched vs. Matched"] = t_test_results["UnMatched vs. Matched"]
# Was there significance between extroverts who got targeted ads vs. extroverts who got untargeted ads?
final_results["ExtrovertsWhoGotTargeted vs. ExtrovertsWhoGotUnTargeted"] = t_test_results["ExtrovertsWhoGotTargeted vs. ExtrovertsWhoGotUnTargeted"]
# Was there significance between introverts who got targeted ads vs. introverts who got untargeted ads?
final_results["IntrovertsWhoGotTargeted vs. IntrovertsWhoGotUnTargeted"] = t_test_results["IntrovertsWhoGotTargeted vs. IntrovertsWhoGotUnTargeted"]
# Was there significance between general people who were targeted vs. untargeted?
final_results["Targeted vs. UnTargeted"] = t_test_results["Targeted vs. UnTargeted"]
# Was there signficance betweeen matched and targeted vs. matched and untargeted?
final_results["MatchedTargeted vs. MatchedUnTargeted"] = t_test_results["MatchedTargeted vs. MatchedUnTargeted"]
# Was there signficance betweeen unmatched and targeted vs. unmatched and untargeted?
final_results["UnMatchedTargeted vs. UnMatchedUnTargeted"] = t_test_results["UnMatchedTargeted vs. UnMatchedUnTargeted"]
# Was there signficance betweeen matched and untargeted vs. unmatched and untargeted?
final_results["MatchedUnTargeted vs. UnMatchedUnTargeted"] = t_test_results["MatchedUnTargeted vs. UnMatchedUnTargeted"]

print(final_results)
significant_test_reults = {}
for i in final_results.keys():
    if final_results[i]['p'] <= 0.05:
        significant_test_reults[i] = final_results[i]
        print(i, '     ', final_results[i])








