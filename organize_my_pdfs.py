#!/usr/bin/env python3
# got through all pdfs in /Users/albert/Documents/SwiftScan and check with `pdftotext <file> -` if file is ORC'd, if not, detect language (if fra, eng, deu) and use ocrmypdf for ORC'ing.
# from operator import is_
import os
import subprocess
import re
import sys
import pprint
import shutil
import argparse


def help(p = None):
    string = ''' helptext '''
    p = argparse.ArgumentParser(description=string,
            formatter_class=argparse.RawTextHelpFormatter)
    #p.add_argument('-i','--input_file', required=True, type=str,default=False, help="path to the input_file")
    p.add_argument('-f',      '--file', help='path to the input file', action='store', default=False)
    p.add_argument('-v',       '--verbose', help='verbose', action='count', default=False)
    p.add_argument('-d',       '--debug', help="Enable debug logging.", action='store_true')
    return p
# from isort import file
# from pytz import NonExistentTimeError

def printcolor(*message, color="green", style="None", **kwargs):
    """Print with selected color.

    in 1;42;31m
       |---> 1: style {0-8} : {
        0:None,
        1:bold,
        2:thinnest/faint,
        3:italic,
        4:underlined,
        5:blink,
        6:blink2,
        7:colored backgrount,
        9:strike through
        }
    in 1;42;31m
             |---> 31: colors {30-38,91}= {
                 'gray':30,
                 'red':31,
                 'green':32,
                 'orange':33,
                 'blue':34,
                 'pink':35,
                 'magenta':36,
                 'turquoise':36,
                 'white':37,
                 'orangereal':91}
    n 1;42;31m
         |---> 42: background {39-48}= {}
    Args:
        color (str, optional): _description_. Defaults to 'green'.
    """
    styles = {
        "None": 0,
        "bold": 1,
        "faint": 2,
        "italic": 3,
        "underline": 4,
        "blink": 5,
        "blink2": 6,
        "colored-background": 7,
        "strike-through": 9,
    }
    colors = {
        "gray": 30,
        "red": 31,
        "green": 32,
        "orange": 33,
        "blue": 34,
        "pink": 35,
        "magenta": 36,
        "turquoise": 36,
        "white": 37,
        "orangereal": 91,
        "lila": 95,
    }
    # background = {
    #     "None": 38,
    #     "gray": 40,
    #     "red": 41,
    #     "green": 42,
    #     "orange": 43,
    #     "blue": 44,
    #     "pink": 45,
    #     "magenta": 46,
    #     "white": 47,
    # }
    # print('color,',color,'->',str(colors[color]))
    message2 = " ".join(map(str, message))

    # if color == 'green':    color_ = '\x1b[6;32;40m'
    # if color == 'red':      color_ = '\x1b[6;33;31m'
    # if color == 'rednew':      color_ = '\x1b[6;33;33m'
    # if color == 'orange':   color_ = '\x1b[6;33;33m'
    # if color == 'purple':   color_ = '\x1b[6;33;35m'
    # if color == 'blue':     color_ = '\x1b[6;34;44m'
    # if color == 'redbg':    color_ = '\x1b[6;37;41m'
    # color_ = '\x1b[6;37;'+str(colors[color])+'m'
    color_ = "\x1b[" + str(styles[style]) + ";37;" + str(colors[color]) + "m"
    # print('color_',color_)
    # print('kk')
    # print(color_ + message2 + "\x1b[0m", **kwargs)
    print(color_ + message2 + "\33[0m", **kwargs)
    return


def printred(*message, **kwargs):
    """Print red."""
    return printcolor(*message, **kwargs, color="red")

def printgreen(*message, **kwargs):
    """Print green."""
    return printcolor(*message, **kwargs, color="green")

def printblue(*message, **kwargs):
    """Print blue."""
    return printcolor(*message, **kwargs, color="blue")


def is_orc_pdf(file_path):
    """Check if a PDF file is OCR'd."""
    text = ""
    try:
        output = subprocess.check_output(['pdftotext', file_path, '-'], stderr=subprocess.STDOUT)
        text = output.decode('utf-8').strip()
    except:
        text = ""
    
    # print(file_path,":"+text+":")
    
    if text == "":
        # print("NO, it is NOT OCR'd")
        return False, False
    else:       
        # print("YES, it is OCR'd")
        return True,text

def extract_re_from_line(get_value,line,args):
    # Extract the month.year part
    match = re.search(get_value, line)
    if args.verbose:
        printblue('>>line     :',line)
    
    if args.verbose:
        printblue('>>get_value:',get_value)
        printblue('>>match    :',match)
    if match:
        # Extract just the [0-9][0-9].20[0-9][0-9] part
        # found = re.search(r'[0-9][0-9]\.20[0-9][0-9]', line).group()
        text = re.search(get_value, line).group()
        if args.verbose:
            print('>>text     :',text)
        text2 = text.replace(' ', '_')
        if args.verbose:
            print('>>text2  :',text2)  # Output: 12.2024
        text3 = text2.replace('.', '_')
        if args.verbose:
            print('>>text3  :',text3)  # Output: 12_2024
        # Replace __
        
        text4 = text3.replace('__', '_')
        if args.verbose:
            print('>>text4  :',text4)  # Output: 12_

        def clean_string(text):
            # Keep letters, numbers, and dots; remove everything else
            # return re.sub(r'[^a-zA-Z0-9.]', '', text)
            return re.sub(r'[^a-zA-Z0-9._]', '', text)
        found = clean_string(text4)
        if args.verbose:
            print('>>found  :',found)  # Output: 12.2024
        # remove leading and trailing "_"
        found = found.strip('_')
        if args.verbose:
            print('>>found  :',found)

        return found
    else:
        # print("No match found")
        return False
    
def make_sure_file_is_orcd(file_path):
    # make sure it is orc
    is_orc, text = is_orc_pdf(file_path)
    if is_orc:
        # printgreen(file_path)
        pass
    else:
        printblue(file_path,'-> ORCing ...')
        subprocess.check_call(['ocrmypdf', file_path, file_path + '.ocr.pdf'])
        is_orc, text = is_orc_pdf(file_path+'.ocr.pdf')
        if is_orc:
            os.replace(file_path+'.ocr.pdf', file_path)
            printgreen(file_path + ' -> OCR applied')
        else:
            printred(file_path + ' -> OCR failed')
            sys.exit('234')
    return is_orc, text


def get_yes_no_red():
    return input("\x1b[0;37;31m"+"[??]      : >> [y]es / [n]o : "+"\33[0m")

def phrases_get_empty():
    '''count how many of the phrases given below are contained in text.'''
    phrases = { 'APEMS_bill_L_J'  : { 'search'  : [ 'APEMS', 'Corminjoz', 'Prestations pour', 'Glensk', 'Laura','Jakob', 'Montant CHF', 'Factur' , 'Facturation' ],
                                        'get_all' : [{'Facturation': r'[0-9][0-9]\.(20[0-9][0-9]|[0-9][0-9])', 'replace': False}],
                                        'filename': 'Rechnung_<Facturation>_Jakob_und_Laura.pdf',
                                        'folder'  : '/Users/albert/Documents/Vertraege_Versicherungen/Kinder_APEMS/2025/',
                                    },
                'Sorbier_bill_S_E'   : { 'search'  : [ 'Sorbiers', 'Prestations pour', 'Glensk', 'Simon','Emil', 'Montant CHF', 'Factur' , 'Facturation' ],
                                        'get_all' : [{'Facturation': r'[0-9][0-9]\.(20[0-9][0-9]|[0-9][0-9])', 'replace': False}],
                                        'filename': 'Rechnung_<Facturation>_Simon_und_Emil.pdf',
                                        'folder'  : '/Users/albert/Documents/Vertraege_Versicherungen/Kinder_Sorbier/2025/',
                                    },
                'Sorbier_contrat_S_E'   : { 'search'  : [ 'Sorbiers', 'Contrat', 'Glensk','Emil','Signatures','R.f'],
                                        'get_all' : [{'Contrat': r'.*du.*au.*', 'replace': False}, {'R.f': r'^[rR].[Ff].*[0-9][0-9$]', 'replace': False} ],
                                        'filename': 'Vertrag_<Contrat>_<R.f>_Simon_und_Emil.pdf',
                                        'folder'  : '/Users/albert/Documents/Vertraege_Versicherungen/Kinder_Sorbier/2025/',
                                    },
                'APEMS_contrat_J_L'   : { 'search'  : [ 'APEMS', 'Contrat','valable' 'Glensk','Laura','Jakob','Signatures','R.f'],
                        'get_all' : [{'Contrat': r'^[Cc][Oo][Nn][tT][rR][Aa][tT].*', 'replace': False}, \
                                     {'R.f': r'^[rR].[Ff].*[0-9][0-9$]', 'replace': False}, \
                                     {'valable':r'^[Vv][Aa][Ll][Aa][Bb][Ll][Ee].*le.*au.*', 'replace': False}],
                        'filename': 'Vertrag_<Contrat>_<valable>_<R.f>_Jakob_und_oder_Laura.pdf',
                        'folder'  : '/Users/albert/Documents/Vertraege_Versicherungen/Kinder_APEMS/2025/',
                    },
                                      
                # 'APEMS_contract'    : {'search'   : [ 'APEMS', 'Corminjoz', 'Contrat' ],
                #                        'get_all'  : [{}],
                #                        'filename' : 'Vertrag_',
                #                        'folder'   : '/Users/albert/Documents/Vertraege_Versicherungen/???/'
                #                     },
              }
    
    # phrases = {}
    for key, value in phrases.items():
        # print('key',key,'value',value)
        # phrases[key] = {'search': value['search'], 
        #                 'get_all':value['get_all'], 
        #                 'count': 0, 
        #                 'found': [], 'probability' : 0}
        phrases[key]['count'] = 0
        phrases[key]['found'] = []
        phrases[key]['probability'] = 0
    return phrases

def phrases_evaluate(text,args):
    phrases = phrases_get_empty()
    # print("> 1 > ",phrases)
    
    # get ist of all phrases that are in phrases
    for key, value in phrases.items():
        phrases_ = phrases[key]['search'] 
        
        for phrase in phrases_:
            if re.search(phrase, text, re.IGNORECASE):
                phrases[key]['count'] += 1
                phrases[key]['found'].append(phrase)
                # print("aa",phrases[key]['found'])
                # print('bb',len(phrases[key]['found']))
                phrases[key]['probability'] = int(100*len(phrases[key]['found'])/len(phrases[key]['search']))
            
    # print("> 2 > ",phrases)
    # sys.exit('23434')
    for key, value in phrases.items(): 
        # key = APEMS_bill, APEMS_contract; 
        # values = {'count':9, 'found' = [...], 'get_all' = [..], 'probability'}
        # print(key.ljust(20),str(phrases[key]['probability']).ljust(3)+" %")
        # if phrases[key]['probability'] > 65:
        if True:
            # print("key",key)
            get_all = phrases[key]['get_all']
            # go line by line through text using readlines
            lines = text.split('\n')
            for line in lines:
                # print()
                # print(">>line       :",line)
                # print(">>get_all    :",get_all)
                
                for item in get_all:
                    # print('>>item       :',item)
                    for get_key, get_value in item.items():
                        if get_key == 'replace':
                            continue
                        # print(">>get_all    :",get_all)
                        # print('>>item       :',item)
                        # print(">>get_key    :",get_key)
                        # print(">>get_value  :",get_value)
                        
                        if re.search(get_key, line, re.IGNORECASE):
                            # if False: #True: #False:
                            if args.verbose:
                                print()
                                print(">>line       :",line)
                                print(">>get_all    :",get_all)
                                print('>>item       :',item)
                                print(">>get_key    :",get_key)
                                print(">>get_value  :",get_value)
                                # GroK prompt: in python: I have following variables: line='Facturation 12.2024' and I am having a variable get_value='Facturation [0-9][0-9].20[0-9][0-9]' which is a regular expression that defines what I want to get out, which is whatever the value is that '[0-9][0-9].20[0-9][0-9]' fits. can you give me the python code to extract the month.year
                                # line = 'Facturation 12.2024'
                                # get_key = 'Facturation'
                                # get out Month and Year
                            found = extract_re_from_line(get_value,line,args)
                            if args.verbose:
                                print('>> replacing??',found)
                            
                            # sys.exit('33')
                            if found:
                                if args.verbose:
                                    print('>> replacing?',found)
                                if item['replace'] == False:
                                    printblue('>> replacing!',found)
                                    item['replace'] = found
                                    # print("phrases",phrases)
                                    # pprint.pprint(phrases)
                                else:
                                    print("item",item)
                                    print("found",found)
                                    sys.exit('get_all was already filled when I found another value')
                            
                            
                            # sys.exit('asasdf')
                # find regular expression 'Facturation [0-9][0-9].[0-9][0-9]' in the text to  get month and year for renaming filename
                # print('line done')
    return phrases


    
def get_best_candidate(phrases):
    best_candidate = ['None',0,0]
    for key, value in phrases.items(): 
        # key = APEMS_bill, APEMS_contract; 
        # values = {'count':9, 'found' = [...], 'get_all' = [..], 'probability'}
        probability_item = phrases[key]['probability'] 
        if probability_item < 50:
            continue
        probability_before = best_candidate[1]
        
        if probability_item > best_candidate[1]:
            best_candidate = [key,probability_item,1]
        elif probability_item == best_candidate[1]:
            if probability_item == 0:
                #     best_candidate = [None,0,0]
                pass
            else:
                best_candidate = [key,probability_item,1+best_candidate[2]]
        
    # printgreen(best_candidate)

    if best_candidate[2] == 1: # the highest probability is there just one time
        return best_candidate
    elif best_candidate[1] == 0: # no match found
        return best_candidate
    else:
        print('best_candidate',best_candidate)
        pprint.pprint(phrases)
        sys.exit('best candidate is not sure which, there seems to be other contenders')
    

def substitute_filename(filename, subst_what, subst_with):
    return filename.replace(f'<{subst_what}>', subst_with)        

def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        printgreen(f"File moved from {source_path} to {destination_path}")
    except FileNotFoundError:
        print(f"Error: Source file {source_path} not found")
    except Exception as e:
        print(f"Error: {e}")
        

def process_pdfs(directory,args):
    """Process all PDF files in a directory."""
    if args.file:
        files_gothrough = [args.file]
    else:
        # print("1")
        files_gothrough = []
        for root, dirs, files in os.walk(directory):
            for filename in files:
                # print("filename",filename)
                if filename.endswith('.pdf'):
                    files_gothrough.append(os.path.join(root, filename))

    # print("files_gothrough",files_gothrough)
    # sys.exit()              
    for file_path in files_gothrough:  
        #######################
        # make sure it is orc
        ########################        
        is_orc, text = make_sure_file_is_orcd(file_path)
        if not is_orc: sys.exit('not orcd')
        
        ##################################
        # go thorugh the lines of the text
        ###################################
        phrases = phrases_evaluate(text,args)
        if args.verbose:
            printblue('>>phrases:')
            pprint.pprint(phrases)
            print()
        # sys.exit('asdfasd')
        
        bc = get_best_candidate(phrases)
        print()
        printgreen('best_candidate 786:',bc[0].ljust(15),str(bc[1]).ljust(3),bc[2],file_path)
        # if file_path == '/Users/albert/Documents/SwiftScan/SwiftScan_2025-06-15_13.16.52.pdf':
        #     pprint.pprint(phrases)
        #     sys.exit("asdfasd77777")
        verbose = False
        verbose = True
        if bc[1] > 49:
            # pprint.pprint(phrases)
            if verbose:
                print("--")
            getitem = phrases[bc[0]]
            if verbose:
                pprint.pprint(getitem)
                print("--")
                print('full:')
                pprint.pprint(phrases)
                
            ########## make the filename
            folder = getitem['folder']
            if verbose:
                print("?? folder",folder)
            filename_to_substitute = getitem['filename']
            if verbose:
                print("?? filename_to_substitute",filename_to_substitute)
            if not os.path.isdir(folder):
                printgreen("Do you want to create the folder "+folder+" first?")
                sys.exit('774')
            get_all = getitem['get_all']
            if verbose:
                print("?? get_all",get_all)
            for idx,item in enumerate(get_all):
                if verbose:
                    print()
                    print("?? item",idx,item)
                subst_what = False
                subst_with = False
                for key, value in item.items():
                    if verbose:
                        #for key,value in getitem['get_all']: # get: {'Facturation': 'Facturation [0-9][0-9]\\.20[0-9][0-9]','replace': '12.2024'}
                        print("?? 11 key",key)
                        print("?? 11 value",value)
                    if key == 'replace' and subst_with == False:
                        subst_with = value
                    elif key != 'replace' and subst_what == False:
                        subst_what = key
                if verbose:
                    print("?? 22 subst_what",subst_what)
                    print("?? 22 subst_with",subst_with)
                    print("?? 33 ==>",filename_to_substitute,subst_what,subst_with)
                filename_to_substitute = substitute_filename(filename_to_substitute, subst_what, subst_with)
                if verbose:
                    print("?? 44 ==> filename_to_substitute:", filename_to_substitute) 
                    print()

            filename_new = filename_to_substitute # substitute_filename(filename_to_substitute, subst_what, subst_with)
            if verbose:
                print("?? filename_new",filename_new)  # Output: Rechnung_12.2024_Jakob_und_Laura.pdf
            # Grok: python; filename_to_substitute='Rechnung_<Facturation>_Jakob_und_Laura.pdf'; subst_what='Facturation';subst_with='12.2024';subst stands for substitute; can you write me a function in python that substitutes the <item> in filename_to_substitute from subst_what with the string in subst_with so that I get out filename_to_substitute_new='Rechnung_12.2024_Jakob_und_Laura.pdf';
            file_path_new = folder+'/'+filename_new
            if verbose:
                print("?? file_path_new",file_path_new)
            printred(' '*36,file_path,'->',file_path_new)
            if '<' in file_path_new or '>' in file_path_new:
                pprint.pprint(phrases)
                sys.exit("?? file_path_new contains '< >'")
            # pprint.pprint(phrases)
            
            # sys.exit('==> should I move it? a-0sd')
            if bc[1] >= 98:
                answer = 'y'
            elif bc[1] >= 50:
                answer = get_yes_no_red()
            else:
                printred('Skipping file', file_path, 'because probability is too low:', bc[1])
                continue
            
            if answer.lower() in ['y', 'yes', 'j', 'ja']:
                printgreen('Moving file to', file_path_new)
                if os.path.isfile(file_path_new):
                    print('??file_path_new',file_path_new,'does already exist!')
                    sys.exit("path does exist already!")
                    
                move_file(file_path, file_path_new)
            else:
                printred('Skipping file', file_path)
                continue
                
                # sys.exit("asdfasdf7888")
            # sys.exit('done')
            
        # if file_path == '/Users/albert/Documents/SwiftScan/SwiftScan_2025-03-16_15.25.15.pdf':
        #     sys.exit('00800i0i')
    
# sys.exit("get this right first")
                

if __name__ == "__main__":
    p = help()
    args = p.parse_args()
    process_pdfs('/Users/albert/Documents/SwiftScan',args=args)