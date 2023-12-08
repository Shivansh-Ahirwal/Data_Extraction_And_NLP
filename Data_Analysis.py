import glob
import pandas as pd
import syllapy
import re

def stop_words_list():
    stopword_files = (glob.glob(r'C:\Users\Sachi\sunny projects\blackcoffee_project\stop_words'+'/*.txt'))
    stopwords = []

    for file in stopword_files:
        open_file = open(file,'r',encoding = 'latin-1')
        stoptext = open_file.read()
        stoptext = stoptext.replace('|','\n').split("\n")
        stopwords = stopwords + stoptext  
    return stopwords
    
def remove_stopwords(stopwords,word_list):
    for words in stopwords:
        if words in word_list:
            word_list.remove(words) 
    return(word_list) 
        
def Whole_Analysis(stopwords,positive_text,negative_text,file_path,urls):        
    for i in range(0,113):
        positive_score = 0
        negative_score = 0
        url_id = urls['URL_ID'][i]
        url = urls['URL'][i]
        file = open(file_path + str(urls['URL_ID'][i]),'r',encoding='utf-8')
        text = file.read()
        skip = {",",":",";","'",'"'}
        for ch in skip:
            text = text.replace(ch,"")
        text2 = text.split(".")
        text.replace(".","")
        text = text.split(" ")
        for i in positive_text:
            if i in text:
                positive_score+=1
        
        for i in negative_text:
            if i in text:
                negative_score+=1
        
        for words in stopwords:
            if words in text:
                text.remove(words)
            
        polarity =  (positive_score-negative_score) / ((positive_score + negative_score) + 0.000001)
        
        subjectivity = (positive_score + negative_score)/ (len(text) + 0.000001)
        
        complex_words = []
        for words in text:
            if (syllapy.count(words))>2:
                complex_words.append(words)
                
        avg_sentence_length = len(text)/len(text2)
        
        per_of_complex_words = len(complex_words)/len(text)
        
        fog_index = 0.4 * (avg_sentence_length + per_of_complex_words)
        
        avg_num_of_words_per_sent = len(text)/len(text2)
        
        complex_count = len(complex_words)
        
        word_count = len(text)
        
        syllable_count = 0
        for i in text:
            if i.endswith(('es','ed')):
                continue
            else:
                syllable_count += syllapy.count(i)
                
        # Define a regex pattern for personal pronouns
        pronoun_pattern = re.compile(r'\b(?:I|we|my|ours|us)\b', flags=re.IGNORECASE)

        # Use the findall method to count occurrences of the pronouns in the text
        personal_pronoun = len(pronoun_pattern.findall(text))
        
        total_ch = 0
        for i in text:
            total_ch += len(i)
            
        avg_word_length = total_ch / word_count
        
        data_dict = {"URL_ID": url_id,"URL": url,"positive_score":positive_score,"negative_score":negative_score,"polarity_score":polarity,"subjectivity_Score":subjectivity,"avg_sentence_length":avg_sentence_length,"per_of_complex_num":per_of_complex_words,"fog_index":fog_index,"avg_num_of_words_per_sent":avg_num_of_words_per_sent,"complex_word_count":complex_count,"word_count":word_count,"syllable_count_per_word":syllable_count,"personal_pronoun":personal_pronoun,"avg_word_length":avg_word_length}
        data_list = []
        data_list.append(data_dict)
    return(data_list)

def list_to_excelsheet(data_list):    
    
    excel_file = r"C:\Users\Sachi\sunny projects\blackcoffee_project\blackcoffer_output.xlsx"
    df = pd.DataFrame(data_list)
    df.to_excel(excel_file,index = False)

def main():
    
    urls = pd.read_csv("C:\\Users\\Sachi\\Downloads\\Input.xlsx - Sheet1.csv")
    file_path = 'C:\\Users\\Sachi\\sunny projects\\blackcoffee_project\\output_files\\'

    #seperating negative word to compare them with the words in the file.
    positive_file = open("C:\\Users\\Sachi\\sunny projects\\blackcoffee_project\\positive-words.txt",'r',encoding = "utf-8")
    positive_text = positive_file.read()
    positive_text = positive_text.split("\n")

    #seperating negative word to compare them with the words in the file.
    negative_file = open("C:\\Users\\Sachi\\sunny projects\\blackcoffee_project\\negative-words.txt",'r',encoding = "utf-8")
    negative_text = negative_file.read()
    negative_text = negative_text.split("\n")

    stopwords = stop_words_list()

    positive_text = remove_stopwords(stopwords,positive_text)
    negative_text = remove_stopwords(stopwords,negative_text)

    data_list = Whole_Analysis(stopwords=stopwords,positive_text=positive_text,negative_text=negative_text,file_path=file_path,urls=urls)

    list_to_excelsheet(data_list=data_list)

if "__name__" == "__main__":
    main()