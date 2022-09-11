# Language recognition via monograms

This is a language recognition model based on the simplest approach - analyzing the frequency of letters.
This method is far from accurate and does not work well with short texts.

It also implements a convenient procedure for automatically adding new languages when generating the model.
Below is described how to prepare data for it so that it works correctly.
Or you can immediately look at some of the files in [`/data`](https://github.com/vsha96/language_recognition/tree/main/data), the structure is quite simple.

The algorithm operation is described in detail in the [`language_recognition.ipynb`](https://github.com/vsha96/language_recognition/blob/main/language_recognition.ipynb) (RU)



## Installation

- clone this repo  
`git clone git@github.com:vsha96/language_recognition.git`
- import the module  
```python
import mylangrec as mlr
```

#### Required modules:
csv, re, pickle, numpy



## Usage

See examples in the [`main.py`](https://github.com/vsha96/language_recognition/blob/main/main.py)

#### Recognition:
Works out of the box. If you haven't deleted `obj/langrec_monograms.pkl`.

- Model assembly procedure:
`lang_generate()`
- Recognition functions: `recog("there is a string")` or `recog_file(file_path)`

#### Automatic language adding:

- Add a file with the frequencies of the language in the [`/data`](https://github.com/vsha96/language_recognition/tree/main/data) with the name `<language>_*.txt` (see examples in the [`/data`](https://github.com/vsha96/language_recognition/tree/main/data))  
! an absolute or relative frequency (one of two) must be specified for each letter of the language inside the file
- Invoke 
`lang_generate()`
- See the new files for the languages inside [`/languages`](https://github.com/vsha96/language_recognition/tree/main/languages)




