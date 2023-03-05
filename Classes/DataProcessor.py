import pandas as pd 

class DataProcecssor():
    """
    This class processes the data from our qualtrics survey for our 397 - Data Privacy Class 

    All of the methods are private, but the following fields will be useful:
    -  self.introvert_counts -> Response counts of all introverts
    -  self.extrovert_counts -> Response counts of all extroverts 

    -  self.introvert_who_got_introvert_counts -> Response counts of introverts who got the introverted ad 
    -  self.extrovert_who_got_extrovert_counts  -> Response counts of extroverts who got the extroverted ad 
    -  self.introverts_who_got_extrovert_counts -> Response counts of introverts who got the extroverted ad 
    -  self.extrovert_who_got_introvert_counts -> Response counts of extroverts who got the introverted ad 

    -  self.introverts_who_got_introvert_ad_untargeted_counts -> Response counts of introverts who got the introverted ad and were told it was untargeted
    -  self.introverts_who_got_extrovert_ad_untargeted_counts -> Response counts of introverts who got the extroverted ad and were told it was utargeted
    -  self.introverts_who_got_introvert_ad_targeted_counts -> Response counts of introverts who got the introverted ad and were told it was targeted
    -  self.introverts_who_got_extrovert_ad_targeted_counts -> Response counts of introverts who got the extroverted ad and were told it was targeted
    
    -  self.extroverts_who_got_introvert_ad_untargeted_counts -> Response counts of extroverts who got the introverted ad and were told it was untargeted
    -  self.extroverts_who_got_extrovert_ad_untargeted_counts -> Response counts of extroverts who got the extroverted ad and were told it was untargeted
    -  self.extroverts_who_got_introvert_ad_targeted_counts -> Response counts of extroverts who got the introverted ad and were told it was targeted
    -  self.extroverts_who_got_extrovert_ad_targeted_counts -> Response counts of extroverts who got the extroverted ad and were told it was targeted

    -  self.introverts_who_got_introvert_ad_untargeted -> All data rows for introverts who got the introverted ad and were told it was untargeted
    -  self.introverts_who_got_extrovert_ad_untargeted -> All data rows for introverts who got the extroverted ad and were told it was untargeted
    -  self.introverts_who_got_introvert_ad_targeted  -> All data rows for introverts who got the introverted ad and were told it was targeted
    -  self.introverts_who_got_extrovert_ad_targeted  -> All data rows for introverts who got the extroverted ad and were told it was targeted

    -  self.extroverts_who_got_introvert_ad_untargeted -> All data rows for extroverts who got the introverted ad and were told it was untargeted
    -  self.extroverts_who_got_extrovert_ad_untargeted -> All data rows for extroverts who got the extroverted ad and were told it was untargeted
    -  self.extroverts_who_got_introvert_ad_targeted  -> All data rows for extroverts who got the introverted ad and were told it was targeted
    -  self.extroverts_who_got_extrovert_ad_targeted  -> All data rows for extroverts who got the extroverted ad and were told it was targeted

    -  self.extroverts_who_got_targeted_counts -> All extroverts who got a targeted ad 
    -  self.introverts_who_got_targeted_counts -> All introverts who got a targeted ad 
    -  self.extroverts_who_got_untargeted_counts -> All extroverts who got an untargeted ad 
    -  self.introverts_who_got_untargeted_counts -> All introverts who got an untargeted ad 

    -  self.targeted_counts -> Everyone who got a targeted ad 
    -  self.untargeted_counts -> Everyone who got an untargeted ad 

    -  self.matched_untargeted_counts -> All people who got a matched ad that said it was untargeted 
    -  self.matched_targeted_counts -> All people who got a matched ad that said it was targeted 
    -  self.unmatched_untargeted_counts -> All people who got an umatched ad that said it was untargeted 
    -  self.unmatched_targeted_counts -> All people who got an umatched ad that said it was targeted 

    -  self.matched_counts -> All people who got an ad that matched their introversion/extroversion 
    -  self.unmatched_counts -> All people who got an ad that didn't match their introversion/extroversion



    - self.data -> A dataframe containing all valid rows with added columns [IntrovertExtrovert, AdMatchedUnmatched, TargetedUntargeted, 'Response'] 
                   which stores values for statistical analysis purposes 
    """
    def __init__(self) -> None:
        self.response_to_num = {'Extremely unlikely': 0, "Somewhat unlikely": 1,'Neither likely nor unlikely':2, 'Somewhat likely': 3, 'Extremely likely': 4 }
        self.raw_data = self.__load_data__()
        self.ratings_w_rows = {"Introvert":[],"Extrovert":[],"Neutral":[],"Inconclusive":[]}

        #Iterate through and score the first 18 questions for each valid response, store score in self.ratings_w_rows()
        for index, row in self.raw_data.iterrows():
            if row['Status'] != 'IP Address':
                continue
            score = self.__introvert_or_extrovert__(row)
            self.ratings_w_rows[score].append(row)

        #Set up some overarching groups 
        self.introvert_counts = {'Name': 'Introverts', 'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extrovert_counts = {'Name': 'Extroverts', 'Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        
        self.introvert_who_got_introvert_counts = {'Name': 'IntrovertsWhoGotIntrovertAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extrovert_who_got_extrovert_counts = {'Name': 'ExtrovertsWhoGotExtrovertAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_extrovert_counts = {'Name': 'IntrovertsWhoGotExtrovertAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extrovert_who_got_introvert_counts = {'Name': 'ExtrovertsWhoGotIntrovertAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        
        #Split introverts into the 4 ad groups 
        self.introverts_who_got_introvert_ad_untargeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q26'] != -1]
        self.introverts_who_got_extrovert_ad_untargeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q25'] != -1]
        self.introverts_who_got_introvert_ad_targeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q34'] != -1]
        self.introverts_who_got_extrovert_ad_targeted = [i for i in self.ratings_w_rows['Introvert'] if i['Q24'] != -1]

        #Add relevant fields 
        for i in self.introverts_who_got_introvert_ad_untargeted:
            i['AdMatchedUnmatched'] = 1 # 1 means True, ad was matched 
            i['TargetedUntargeted'] = 0 # 0 means False, untargeted 
        for i in self.introverts_who_got_extrovert_ad_untargeted:
            i['AdMatchedUnmatched'] = 0
            i['TargetedUntargeted'] = 0
        for i in self.introverts_who_got_introvert_ad_targeted:
            i['AdMatchedUnmatched'] = 1
            i['TargetedUntargeted'] = 1
        for i in self.introverts_who_got_extrovert_ad_targeted:
            i['AdMatchedUnmatched'] = 0
            i['TargetedUntargeted'] = 1
        

        self.introverts_who_got_introvert_ad_untargeted_counts = {'Name': 'IntrovertsWhoGotUntargetedtIntrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_extrovert_ad_untargeted_counts = {'Name': 'IntrovertsWhoGotUntargetedtExtrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_introvert_ad_targeted_counts = {'Name': 'IntrovertsWhoGotTargetedtIntrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_extrovert_ad_targeted_counts = {'Name': 'IntrovertsWhoGotTargetedtExtrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }

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

        #Add relevant fields 
        for i in self.extroverts_who_got_introvert_ad_untargeted:
            i['AdMatchedUnmatched'] = 0
            i['TargetedUntargeted'] = 0
        for i in self.extroverts_who_got_extrovert_ad_untargeted:
            i['AdMatchedUnmatched'] = 1
            i['TargetedUntargeted'] = 0
        for i in self.extroverts_who_got_introvert_ad_targeted:
            i['AdMatchedUnmatched'] = 0
            i['TargetedUntargeted'] = 1
        for i in self.extroverts_who_got_extrovert_ad_targeted:
            i['AdMatchedUnmatched'] = 1
            i['TargetedUntargeted'] = 1

        self.extroverts_who_got_introvert_ad_untargeted_counts = {'Name': 'ExtrovertsWhoGotUntargetedtIntrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extroverts_who_got_extrovert_ad_untargeted_counts = {'Name': 'ExtrovertsWhoGotUntargetedtExtrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extroverts_who_got_introvert_ad_targeted_counts = {'Name': 'ExtrovertsWhoGotTargetedtIntrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.extroverts_who_got_extrovert_ad_targeted_counts = {'Name': 'ExtrovertsWhoGotTargetedtExtrovertedAd','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }

        self.__count_responses__(self.extroverts_who_got_introvert_ad_untargeted,self.extroverts_who_got_introvert_ad_untargeted_counts, 'Q26')
        self.__count_responses__(self.extroverts_who_got_extrovert_ad_untargeted,self.extroverts_who_got_extrovert_ad_untargeted_counts, 'Q25')
        self.__count_responses__(self.extroverts_who_got_introvert_ad_targeted,self.extroverts_who_got_introvert_ad_targeted_counts, 'Q34')
        self.__count_responses__(self.extroverts_who_got_extrovert_ad_targeted,self.extroverts_who_got_extrovert_ad_targeted_counts, 'Q24')

        self.__combine_counts__(self.extroverts_who_got_extrovert_ad_targeted_counts,self.extroverts_who_got_extrovert_ad_untargeted_counts, result = self.extrovert_who_got_extrovert_counts)
        self.__combine_counts__(self.extroverts_who_got_introvert_ad_targeted_counts, self.extroverts_who_got_introvert_ad_untargeted_counts, result = self.extrovert_who_got_introvert_counts)
        self.__combine_counts__(self.extroverts_who_got_introvert_ad_untargeted_counts,self.extroverts_who_got_introvert_ad_targeted_counts,self.extroverts_who_got_extrovert_ad_targeted_counts,self.extroverts_who_got_extrovert_ad_untargeted_counts,self.extrovert_counts)

        #Verify 
        # self.__verify_numbers__()
        self.extroverts_who_got_targeted_counts = {'Name': 'ExtrovertsWhoGotTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_targeted_counts = {'Name': 'IntrovertsWhoGotTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.__combine_counts__(self.extroverts_who_got_extrovert_ad_targeted_counts,self.extroverts_who_got_introvert_ad_targeted_counts,result = self.extroverts_who_got_targeted_counts)
        self.__combine_counts__(self.introverts_who_got_extrovert_ad_targeted_counts,self.introverts_who_got_introvert_ad_targeted_counts,result = self.introverts_who_got_targeted_counts)

        self.extroverts_who_got_untargeted_counts = {'Name': 'ExtrovertsWhoGotUnTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.introverts_who_got_untargeted_counts = {'Name': 'IntrovertsWhoGotUnTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.__combine_counts__(self.extroverts_who_got_extrovert_ad_untargeted_counts,self.extroverts_who_got_introvert_ad_untargeted_counts,result = self.extroverts_who_got_untargeted_counts)
        self.__combine_counts__(self.introverts_who_got_extrovert_ad_untargeted_counts,self.introverts_who_got_introvert_ad_untargeted_counts,result = self.introverts_who_got_untargeted_counts)

        self.targeted_counts = {'Name': 'Targeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.untargeted_counts = {'Name': 'UnTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.__combine_counts__(self.extroverts_who_got_targeted_counts,self.introverts_who_got_targeted_counts,result = self.targeted_counts)
        self.__combine_counts__(self.extroverts_who_got_untargeted_counts,self.introverts_who_got_untargeted_counts,result = self.untargeted_counts)

        self.matched_untargeted_counts = {'Name': 'MatchedUnTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.matched_targeted_counts = {'Name': 'MatchedTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.__combine_counts__(self.extroverts_who_got_extrovert_ad_untargeted_counts, self.introverts_who_got_introvert_ad_untargeted_counts,result = self.matched_untargeted_counts)
        self.__combine_counts__(self.extroverts_who_got_extrovert_ad_targeted_counts, self.introverts_who_got_introvert_ad_targeted_counts,result = self.matched_targeted_counts)

        self.unmatched_untargeted_counts = {'Name': 'UnMatchedUnTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.unmatched_targeted_counts = {'Name': 'UnMatchedTargeted','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.__combine_counts__(self.extroverts_who_got_introvert_ad_untargeted_counts, self.introverts_who_got_extrovert_ad_untargeted_counts,result = self.unmatched_untargeted_counts)
        self.__combine_counts__(self.extroverts_who_got_introvert_ad_targeted_counts, self.introverts_who_got_extrovert_ad_targeted_counts,result = self.unmatched_targeted_counts)

        self.matched_counts = {'Name': 'Matched','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 } 
        self.unmatched_counts = {'Name': 'UnMatched','Extremely unlikely': 0, "Somewhat unlikely": 0,'Neither likely nor unlikely':0, 'Somewhat likely': 0, 'Extremely likely': 0 }
        self.__combine_counts__(self.matched_targeted_counts,self.matched_untargeted_counts,result = self.matched_counts)
        self.__combine_counts__(self.unmatched_targeted_counts,self.unmatched_untargeted_counts,result = self.unmatched_counts)
        #Create dataframe with new attributes included
        self.data = self.__create_dataframe__()

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
            row['IntrovertExtrovert'] = result
            return result 
        intrversion = 40 + sum(step1) - sum(step2) 
        if intrversion > 24:  #TODO official was 28
            result = 'Introvert'
        elif intrversion < 25: #TODO official was 20 
            result = 'Extrovert'
        else:
            result = 'Neutral'
        row['IntrovertExtrovert'] = result
        return result 

    def __verify_numbers__(self) -> None:
        print('\nThere are ',len(self.ratings_w_rows['Introvert']), ' introverts before splitting\n','There are ', len(self.ratings_w_rows['Extrovert']), ' Extroverts before splitting \n','There are ', len(self.ratings_w_rows['Neutral']), ' Neutral people before splitting \n')

        print('After splitting there are ', len(self.introverts_who_got_extrovert_ad_targeted) + len(self.introverts_who_got_introvert_ad_targeted) + len(self.introverts_who_got_introvert_ad_untargeted) + len(self.introverts_who_got_extrovert_ad_untargeted), ' introverts')

        print('After splitting there are ', len(self.extroverts_who_got_extrovert_ad_targeted) + len(self.extroverts_who_got_extrovert_ad_untargeted) + len(self.extroverts_who_got_introvert_ad_targeted) + len(self.extroverts_who_got_introvert_ad_untargeted), ' extroverts\n')

    def __count_responses__(self,rows,freqs, question) -> None:
        for row in rows: 
            freqs[row[question]] +=1
            row['Response'] = self.response_to_num[row[question]]
        # print(freqs)

    def __combine_counts__(self,d1,d2,d3 = None ,d4 = None,result = None) -> None:
        for key in result.keys():
            if key == 'Name':
                continue
            if d3 and d4:
                result[key] = d1[key] + d2[key] + d3[key] + d4[key]
            else:
                result[key] = d1[key] + d2[key]

    def __create_dataframe__(self) -> pd.DataFrame:
        lst = self.introverts_who_got_introvert_ad_untargeted + self.introverts_who_got_extrovert_ad_untargeted + self.introverts_who_got_introvert_ad_targeted + self.introverts_who_got_extrovert_ad_targeted
        lst = lst + self.extroverts_who_got_introvert_ad_untargeted + self.extroverts_who_got_extrovert_ad_untargeted + self.extroverts_who_got_introvert_ad_targeted + self.extroverts_who_got_extrovert_ad_targeted
        df = pd.DataFrame(lst)
        return df  