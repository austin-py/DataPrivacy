import pandas as pd 
import statsmodels.api as sm
from statsmodels.formula.api import ols

class DataProcecssor():
    def __init__(self) -> None:
        self.data = self.__load_data__()
        self.ratings_w_rows = {"Introvert":[],"Extrovert":[],"Neutral":[],"Inconclusive":[]}

        #Iterate through and score the first 18 questions for each valid response, store score in self.ratings_w_rows()
        for index, row in self.data.iterrows():
            if row['Status'] != 'IP Address':
                continue
            score = self.__introvert_or_extrovert__(row)
            self.ratings_w_rows[score].append(row)

        self.introvert_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extrovert_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        
        self.introvert_who_got_introvert_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extrovert_who_got_extrovert_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_extrovert_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extrovert_who_got_introvert_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        
        #Split introverts into the 4 ad groups 
        self.introverts_who_got_introvert_ad_untargeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q26'] != -1]
        self.introverts_who_got_extrovert_ad_untargeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q25'] != -1]
        self.introverts_who_got_introvert_ad_targeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q34'] != -1]
        self.introverts_who_got_extrovert_ad_targeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q24'] != -1]

        self.introverts_who_got_introvert_ad_untargeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_extrovert_ad_untargeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_introvert_ad_targeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_extrovert_ad_targeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }

        self.__count_responses__(self.introverts_who_got_introvert_ad_untargeted,self.introverts_who_got_introvert_ad_untargeted_counts, 'Q26')
        self.__count_responses__(self.introverts_who_got_extrovert_ad_untargeted,self.introverts_who_got_extrovert_ad_untargeted_counts, 'Q25')
        self.__count_responses__(self.introverts_who_got_introvert_ad_targeted,self.introverts_who_got_introvert_ad_targeted_counts, 'Q34')
        self.__count_responses__(self.introverts_who_got_extrovert_ad_targeted,self.introverts_who_got_extrovert_ad_targeted_counts, 'Q24')

        self.__combine_counts__(self.introverts_who_got_introvert_ad_targeted_counts,self.introverts_who_got_introvert_ad_untargeted_counts,result = self.introvert_who_got_introvert_counts)
        self.__combine_counts__(self.introverts_who_got_extrovert_ad_targeted_counts,self.introverts_who_got_extrovert_ad_untargeted_counts,result = self.introverts_who_got_extrovert_counts)
        self.__combine_counts__(self.introverts_who_got_extrovert_ad_targeted_counts,self.introverts_who_got_extrovert_ad_untargeted_counts,self.introverts_who_got_introvert_ad_targeted_counts,self.introverts_who_got_introvert_ad_untargeted_counts,self.introvert_counts)
        #Split extroverts into 4 ad groups 
        self.extroverts_who_got_introvert_ad_untargeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q26'] != -1]
        self.extroverts_who_got_extrovert_ad_untargeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q25'] != -1]
        self.extroverts_who_got_introvert_ad_targeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q34'] != -1]
        self.extroverts_who_got_extrovert_ad_targeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q24'] != -1]

        self.extroverts_who_got_introvert_ad_untargeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extroverts_who_got_extrovert_ad_untargeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extroverts_who_got_introvert_ad_targeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extroverts_who_got_extrovert_ad_targeted_counts = {'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }

        self.__count_responses__(self.extroverts_who_got_introvert_ad_untargeted,self.extroverts_who_got_introvert_ad_untargeted_counts, 'Q26')
        self.__count_responses__(self.extroverts_who_got_extrovert_ad_untargeted,self.extroverts_who_got_extrovert_ad_untargeted_counts, 'Q25')
        self.__count_responses__(self.extroverts_who_got_introvert_ad_targeted,self.extroverts_who_got_introvert_ad_targeted_counts, 'Q34')
        self.__count_responses__(self.extroverts_who_got_extrovert_ad_targeted,self.extroverts_who_got_extrovert_ad_targeted_counts, 'Q24')

        self.__combine_counts__(self.extroverts_who_got_extrovert_ad_targeted_counts,self.extroverts_who_got_extrovert_ad_untargeted_counts, result = self.extrovert_who_got_extrovert_counts)
        self.__combine_counts__(self.extroverts_who_got_introvert_ad_targeted_counts, self.extroverts_who_got_introvert_ad_untargeted_counts, result = self.extrovert_who_got_introvert_counts)
        self.__combine_counts__(self.extroverts_who_got_introvert_ad_untargeted_counts,self.extroverts_who_got_introvert_ad_targeted_counts,self.extroverts_who_got_extrovert_ad_targeted_counts,self.extroverts_who_got_extrovert_ad_untargeted_counts,self.extrovert_counts)

        #Verify 
        self.__verify_numbers__()

    def __load_data__(self) -> pd.DataFrame:
        df = pd.read_csv('Data/survey-data.csv')
        df = df.fillna(-1)
        return df 
    
    def __introvert_or_extrovert__(self,row) -> str:
        result = ''
        d = {"Yes": 3, "Undecided": 2, "No": 1,-1:-1}
        step1 = [d[row['Q{}'.format(i)]] for i in [1,4]]
        step2 = [d[row['Q{}'.format(i)]] for i in [2,5,7,8,10,11,13,14,16,18]]
        if -1 in step1 or -1 in step2: 
            result = 'Inconclusive'
            return result 
        intrversion = 40 + sum(step1) - sum(step2) 
        if intrversion > 24:  #TODO official was 28
            result = 'Introvert'
        elif intrversion < 25: #TODO official was 20 
            result = 'Extrovert'
        else:
            result = 'Neutral'
        return result 

    def __verify_numbers__(self) -> None:
        print('There are ',len(self.ratings_w_rows['Introvert']), ' introverts before splitting\n','There are ', len(self.ratings_w_rows['Extrovert']), ' Extroverts before splitting \n','There are ', len(self.ratings_w_rows['Neutral']), ' Neutral people before splitting \n')

        print('After splitting there are ', len(self.introverts_who_got_extrovert_ad_targeted) + len(self.introverts_who_got_introvert_ad_targeted) + len(self.introverts_who_got_introvert_ad_untargeted) + len(self.introverts_who_got_extrovert_ad_untargeted), ' introverts')

        print('After splitting there are ', len(self.extroverts_who_got_extrovert_ad_targeted) + len(self.extroverts_who_got_extrovert_ad_untargeted) + len(self.extroverts_who_got_introvert_ad_targeted) + len(self.extroverts_who_got_introvert_ad_untargeted), ' extroverts')

    def __count_responses__(self,rows,freqs, question) -> None:
        for row in rows: 
            freqs[row[question]] +=1
        # print(freqs)

    def __combine_counts__(self,d1,d2,d3 = None ,d4 = None,result = None) -> None:
        for key in result.keys():
            if d3 and d4:
                result[key] = d1[key] + d2[key] + d3[key] + d4[key]
            else:
                result[key] = d1[key] + d2[key]



#Think we need to re-create a data frame with an 'Introvert' 'Extrovert' Column and their response to the question and then we compare on those two columns basically.




#T test between introverts and extroverts in general 
#T test between introverts who got introvert ad and extrovert ad 
#T test between extroverts who got extrovert ad and introvert ad 