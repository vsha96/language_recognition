import mylangrec as mlr

'''
Model generation procedure (generates language tables, and then the language dictionary itself)
You can only run it, it calls the bottom two procedures.
'''
# mlr.lang_generate()



'''
Procedure for generating language tables from txt files in the `/data` directory
Places tables with language frequencies in the `/languages` directory
'''
# mlr.lang_generate_csv()

'''
The procedure for generating a dictionary of languages
By the contents of the directory `/languages` determines the available languages and makes an object
    `langrec_monograms.pkl`
in the `/obj` directory
'''
# mlr.lang_generate_langrec()



'''
Recognition functions
Output array [language, proximity]
'''

print(mlr.recog('hi how are you?')) # recognize from a string
print(mlr.recog_file('README.txt')) # recognize from a file



