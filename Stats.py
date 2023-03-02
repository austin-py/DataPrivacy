import statsmodels.api as sm
from statsmodels.formula.api import ols

from Classes.DataProcessor import DataProcecssor

dp = DataProcecssor()

model = ols("""Response ~ C(IntrovertExtrovert) + C(AdMatchedUnmatched) + C(TargetedUntargeted)
            + C(IntrovertExtrovert):C(AdMatchedUnmatched) + C(IntrovertExtrovert):C(TargetedUntargeted) + C(AdMatchedUnmatched):C(TargetedUntargeted)
            + C(IntrovertExtrovert):C(AdMatchedUnmatched):C(TargetedUntargeted)""", data = dp.data).fit()

results = sm.stats.anova_lm(model, typ=2)
print(results)

"""
Austin's brief interpretation: 

Since P < 0.05 for AdMatchedUnmatched this likely had a significant effect 

Since P ~ 0.07 for Introvert Extrovert this indicates some effect, but might not reach signfigance 

P ~ 0.18 for Targeted Untargeted so this didn't seem to have a huge effect 

"""