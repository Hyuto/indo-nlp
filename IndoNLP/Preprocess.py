from typing import *
from re import findall, sub
from numpy import asarray, ndarray
from pandas import DataFrame
from emoji import get_emoji_regexp, demojize
from string import punctuation, digits, ascii_lowercase
from tqdm.notebook import tqdm
from urllib.request import urlopen

class FeatureExtraction(object):
    """
    Kelas untuk mengecek beberapa feature dalam text yaitu URL, Hashtags, Tags, dan Emojis
    """
    def __init__(self):
        self.labels, self.encoding = [], {}   # Kelas label dan Encoding 
        self.features = {'urls' : [], 'hashtags' : [], 'tags' : [], 'emojis' : []}   # Feature
        self.patterns = {
            'urls' : ['http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),…]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URL Pattern
                      'www[.](?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),…]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                      r'(?i)\b((?:http[s]?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.])(?:com|net|id|org|info|co)(?:[…/$-_@.&+!*=?]|[0-9a-zA-Z]|[0-9a-zA-Z])+)'],
            'hashtags' : [r'(?i)\#\w+'],  # Hashtag Pattern
            'tags' : [r'(?i)\@\w+'],   # Tags Pattern
            'emojis' : [get_emoji_regexp().pattern]  # Emojis Pattern
        }
    
    @staticmethod
    def search(arr:Union[ndarray, List[str]], patterns:Union[ndarray, List[str]], 
                labels:Union[ndarray, List[str]] = None) -> dict:
        """
        Fungsi Static untuk mencari feature berdasarkan patternya. Jika argument pattern diisi maka akan mengembalikan
        Dictionary dari feature berdasarkan kelasnya.

        Args:
            arr ([np.ndarray, list]): List atau np.ndarray dari teks
            patterns ([np.ndarray, list]): List pattern dari feature yang akan di cari
            labels ([np.ndarray, list], optional): List atau np.ndarray label dari teks. Defaults to None.

        Returns:
            [dict]: Dictionary dari features yang telah di extract dari texts
        """
        res = {}
        # Loop Through
        for i, text in enumerate(arr):
            temp, temp2 = [], []
            for pattern in patterns: # Loop Through
                features = findall(pattern, text) # Cari dari pattern
                temp += features  # simpan ke temp
            # Remove Duplicates
            for feature in temp:
                if temp2 == []:
                    temp2.append(feature)
                else:
                    if all([feature not in x for x in temp2]):
                        temp2.append(feature)
            # Jika labels tidak diisi
            if labels is None:
                for feature in temp2:
                    if feature in res: res[feature] += 1
                    else: res[feature] = 1
            # Jika labels diisi
            else:
                for feature in temp2:
                    if feature in res: 
                        res[feature][labels[i]] += 1
                    else: 
                        res[feature] = {x : 0 for x in sorted(set(labels))}
                        res[feature][labels[i]] += 1
        return res
    
    def get_table(self, feature:Union[ndarray, List[str]], return_prop:bool = False) -> DataFrame:
        """
        Membuat table dari features

        Args:
            feature ([np.ndarray, list, tuple]): Feature mana yang akan dilakukan tabulasi ['urls', 'hashtags', 'tags', 'emojis']
            return_prop (bool, optional): Akan mengembalikan proporsi feature dari masing" kelas jika True.
                                          Jika ingin mengaktifkan feature ini perlu melakukan fitting dengan label. 
                                          Defaults to False.

        Returns:
            [pd.Dataframe]: DataFrame dari Feature
        """
        keys = list(self.features[feature].keys())  # Content data
        values = list(self.features[feature].values()) # Frekuensi data
        if self.labels == []: # Jika fitting tanpa labels
            return (DataFrame({feature : keys, 'frekuensi' : values})
                    .sort_values(by=['frekuensi'], ascending = False).reset_index(drop = True))
        else:
            data = DataFrame({feature : keys}) # Init df
            for label in self.labels: # Loop through
                data[label] = [x[label] for x in values]  # Membuat kolom frekuensi tiap kelasnya
            if return_prop:  # Jika return_prop True
                data['frekuensi'] = data[self.labels].sum(axis = 1).values # Frekuensi total per contentnya
                for label in self.labels:
                    data[label] /= data['frekuensi'] # Membagi Frek dengan Frek total untuk proporsi
                data['max_prop'] = data[self.labels].max(axis = 1).values # Mencari proporsi terbesar 
                return (data.sort_values(by=['frekuensi', 'max_prop'], ascending = False) # Sort dari prop terbesar
                        .reset_index(drop = True))
            return data
    
    def fit(self, arr:Union[ndarray, List[str]], label:Union[ndarray, List[str]] = None, 
            search:str = 'all', return_dict:bool = False) -> dict:
        """
        Fitting terhadap data text. Proses fitting menggunakan label wajib dilakukan jika ingin menggunakan
        keseluruhan fugsi dari kelas ini.

        Args:
            arr ([np.ndarray, list]): List atau np.ndarray dari texts data
            label ([np.ndarray, list], optional): List atau np.ndarray dari kelas pada texts data jika diisi. Defaults to None.
            search (str, optional): List dari feature yang akan dilakukan fitting ['urls', 'hashtags', 'tags', 'emojis'] Auto : 'all'
                                    Jika 'all' maka akan mencari semua feature yang disediakan
            return_dict (bool, optional): Mengembalikan dalam bentuk dict. Defaults to False.

        Returns:
            [dict]: Dictionary dari features jika return_dict == True
        """
        if search == 'all': # Jika search == 'all'
            search = list(self.features.keys())
        if label is not None:
            self.labels = list(sorted(set(label))) # Mendapatkan kelas
        for feature in search: # Search per-Featurenya
            self.features[feature] = self.search(arr, self.patterns[feature], label)
        if return_dict: # return_dict
            return self.features
        
    def build_mask_code(self, min_prop:float = 0, features:str = 'all'):
        """
        Building Mask code dari Feature yang telah di extract.

        Args:
            min_prop (float, optional): Minimal proporsi dari tiap content yang akan di gunakan(di masking). Defaults to 0.
            features (str, optional)  : feature yang akan di decode, meliputi 'urls', 'hashtags', 'tags', dan 'emojis'. 
                                        Defaults to 'all'.

        Raises:
            NotImplementedError: Kelas harus di fit terlebih dahulu dengan label.
        """
        if min_prop and self.labels == [] : raise NotImplementedError("Must fit with labels")
        if features == 'all':
            features = list(self.features.keys())
        for feature in features:
            self.encoding[feature] = {}
            data = self.get_table(feature, return_prop = True)
            if self.labels != []:
                include = sorted(data[feature][data['max_prop'] >= min_prop].tolist(), key = lambda x : len(x),  reverse=True)
                exclude = data[feature][data['max_prop'] < min_prop].values
                for i, words in enumerate(include):
                    self.encoding[feature][words] = f'mask{feature}{i}mask'.upper()
                for i, words in enumerate(exclude):
                    self.encoding[feature][words] = ''
            else:
                include = sorted(data[feature].tolist(), key = lambda x : len(x), reverse = True)
                for i, words in enumerate(include):
                    self.encoding[feature][words] = f'mask{feature}{i}mask'.upper()
        
    def encode(self, array:Union[ndarray, List[str]], features:str = 'all') -> Union[ndarray, List[str]]:
        """
        Encoding data texts dari mask_code yang telah di buat

        Args:
            array ([np.ndarray, list]): List / Numpy array yang berisi kalimat - kalimat yang akan di-encode.
            features (str, optional)  : feature yang akan di decode, meliputi 'urls', 'hashtags', 'tags', dan 'emojis'. 
                                        Defaults to 'all'.

        Raises:
            NotImplementedError: Kelas harus di build_mask_code terlebih dahulu

        Returns:
            [np.ndarray, list]: List / Numpy array yang berisi kalimat - kalimat yang telah di-encode.
        """
        if self.encoding == {} : raise NotImplementedError("Must build mask code first")
        if features == 'all':
            features = list(self.features.keys())
        arr = array.copy()
        for feature in features:
            for i in range(len(arr)):
                for word in self.encoding[feature]:
                    arr[i] = arr[i].replace(word, f' {self.encoding[feature][word]} ')
                arr[i] = ' '.join(arr[i].split())
        return arr
    
    def decode(self, array:Union[ndarray, List[str]]) -> Union[ndarray, List[str]]:
        """
        Decoding data texts yang berisi mask_code kembali

        Args:
            array ([np.ndarray, list]): List / Numpy array yang berisi kalimat - kalimat yang akan di-decode.

        Raises:
            NotImplementedError: Harus fit class terlebih dahulu

        Returns:
            [np.ndarray, list]: List / Numpy array yang berisi kalimat - kalimat yang sudah di-decode.
        """
        if self.encoding == {} : raise NotImplementedError("Must build mask code first")
        features = list(self.features.keys())
        arr = array.copy()
        for feature in features:
            for i in range(len(arr)):
                for word in self.encoding[feature]:
                    if self.encoding[feature][word] != '':
                        arr[i] = arr[i].replace(self.encoding[feature][word], f' {word} ')
                arr[i] = ' '.join(arr[i].split())
        return arr

class SpellChecker(object):
    """
    Mengecek dan memperbaiki misspelling words / kata - kata yang typo pada kalimat -
    kalimat yang ada.
    """
    def __init__(self):
        self.words = {}    # Words

    @staticmethod
    def get_file() -> List[str]:
        """
        Generate .txt file from responsitory.

        Returns:
            [list]: List kata" yang vocabulary yang tersedia untuk dibenarkan.
        """
        data = urlopen("https://raw.githubusercontent.com/Hyuto/NLP/master/Indonesia/kamus/fixed_vocab.txt").read().decode('utf-8')
        return data.split("\n")
        
    def fit(self, direc:str = 'cc-hand-fixed'):
        """
        Fitting untuk mendapatkan vocab yang salah dan vocab yang benar dari file txt

        Args:
            direc (str, optional): Direktori file txt yang berisi vocab. Defaults to 'cc-hand-fixed'.
                                   'cc-hand-fixed' : Catatan Cakrawala Hand Fixed Vocab
        """
        # Read File
        if direc == 'cc-hand-fixed':
            data = self.get_file()
        else:
            f = open(direc, "r")
            data = f.readlines()
            f.close()

        # Main
        for w in data:
            if len(w.split()) == 2:
                missed, true = w.split()
                if '_' in true:
                    true = ' '.join(true.split('_'))
                self.words[missed] = true
        
    def transform(self, arr:Union[ndarray, List[str]]) -> Union[ndarray, List[str]]:
        """
        Mengganti kata - kata yang misspell berdasarkan vocab.

        Args:
            arr ([np.ndarray, list]): List / Numpy array yang berisi kalimat - kalimat yang akan dibenarkan.

        Returns:
            [np.ndarray, list]: Kalimat yang telah di benarkan kata - kata yang misspell
        """
        for i in tqdm(range(len(arr))):
            temp = arr[i].split()
            for j in range(len(temp)):
                if temp[j] in self.words.keys():
                    temp[j] = self.words[temp[j]]
            arr[i] = ' '.join(temp)
        return arr

def clean_up(arr:Union[ndarray, List[str]]) -> Union[ndarray, List[str]]:
    r"""
    Cleanup \n and lowering text

    Args:
        arr ([np.ndarray, list]): Array / list dari kalimat - kalimat.

    Returns:
        [np.ndarray, list]: kalimat tanpa adanya \n dan sudah lowercased.
    """
    for i in range(len(arr)):
        arr[i] = arr[i].lower()
        arr[i] = sub('\n', ' ', arr[i])
        arr[i] = ' '.join(arr[i].split())
    return arr

def normalize(array:Union[ndarray, List[str]], punc_:str = punctuation) -> Union[ndarray, List[str]]:
    """
    Normalisasi penulisan tanda baca

    Args:
        arr ([np.ndarray, list]): Array / list dari kalimat - kalimat.
        punc_ ([str], optional): Tanda Baca. Defaults to string.punctuation

    Returns:
        [np.ndarray, list]: kalimat yang sudah dibenarkan penulisan tanda bacanya.
    """
    punc, arr = punc_, array.copy()
    for i in range(len(arr)):
        temp = list(arr[i])
        for j in range(1, len(temp) - 1):
            if (temp[j] in punc) and not\
            all([x in digits for x in [temp[j-1], temp[j+1]]]):
                temp[j] = ' ' + temp[j] + ' '
            elif (temp[j] in ascii_lowercase) and (temp[j + 1] \
            in digits or temp[j + 1] in punc_):
                temp[j] += ' '
        arr[i] = ''.join(temp)
        arr[i] = ' '.join(arr[i].split())
    return arr

def remove_punc(arr:Union[ndarray, List[str]], punc_:str= punctuation) -> ndarray:
    """
    Menghapus tanda baca pada text.

    Args:
        arr ([np.ndarray, list]): Array / list dari kalimat - kalimat.
        punc_ ([str], optional): Tanda Baca. Defaults to string.punctuation

    Returns:
        [np.ndarray]: kalimat tanpa tanda baca.
    """
    return asarray([x.translate(str.maketrans('', '', punc_))
                    for x in arr])

def deemojized(arr:Union[ndarray, List[str]]) -> Union[ndarray, List[str]]:
    """
    De-Emojized emoji pada string

    Args:
        arr ([np.ndarray, list]): Array / list dari kalimat - kalimat

    Returns:
        [np.ndarray, list]: Kalimat - kalimat
    """
    for i in range(len(arr)):
        arr[i] = demojize(arr[i])
        arr[i] = sub(':', ' ', arr[i])
        arr[i] = sub('_', ' ', arr[i])
        arr[i] = ' '.join(arr[i].split())
    return arr

def RUnecesarry(array:Union[ndarray, List[str]], stopwords:Union[ndarray, List[str]]) -> Union[ndarray, List[str]]:
    """
    Remove Unnecessary words

    Args:
        array ([np.ndarray, list]): Array / list dari kalimat - kalimat
        stopwords([np.ndarray, list, set, tupple]) : Stopwords yang akan di hapus dari text

    Returns:
        [np.ndarray, list]: Kalimat yang sudah di bersihkan
    """
    arr = array.copy()
    for i in range(len(arr)):
        temp = arr[i].split()
        temp = [x for x in temp if not (len(x) == 1 and \
                (x in ascii_lowercase or x in digits))]
        temp = [x for x in temp if x not in stopwords]
        arr[i] = ' '.join(temp).lower()
    return arr