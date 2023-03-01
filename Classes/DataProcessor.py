import pandas as pd 

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
        

        #Split introverts into the 4 ad groups 
        self.introverts_who_got_introvert_ad_untargeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q26'] != -1]
        self.introverts_who_got_extrovert_ad_untargeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q25'] != -1]
        self.introverts_who_got_introvert_ad_targeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q34'] != -1]
        self.introverts_who_got_extrovert_ad_targeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q24'] != -1]

        #Split extroverts into 4 ad groups 
        self.extroverts_who_got_introvert_ad_untargeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q26'] != -1]
        self.extroverts_who_got_extrovert_ad_untargeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q25'] != -1]
        self.extroverts_who_got_introvert_ad_targeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q34'] != -1]
        self.extroverts_who_got_extrovert_ad_targeted = [i for i in self.ratings_w_rows['Extrovert'] if i['Q24'] != -1]

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

        
#TODO Iterate through each of the 8 lists and create a dictionary that holds the response counts for the last question 
#TODO Take that and put it in an ANOVA test 
#TODO Create graphs 
dp = DataProcecssor()