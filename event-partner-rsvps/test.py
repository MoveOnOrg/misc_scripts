import re
import string

PROFANITY_REGEX_ROT = r'?:cvff(?:\\ gnxr|\\-gnxr|gnxr|r(?:ef|[feq])|vat|l)?|dhvzf?|\ofuvg(?:g(?:r(?:ef|[qe])|vat|l)|r(?:ef|[fqel])|vat|[fr])?|g(?:heqf?|jngf?)|jnax(?:r(?:ef|[eq])|vat|f)?|n(?:ef(?:r(?:\\ ubyr|\\-ubyr|ubyr|[fq])|vat|r)|ff(?:\\ ubyrf?|\\-ubyrf?|rq|ubyrf?|vat))|o(?:hyy(?:\\ fuvg(?:g(?:r(?:ef|[qe])|vat)|f)?|\\-fuvg(?:g(?:r(?:ef|[qe])|vat)|f)?|fuvg(?:g(?:r(?:ef|[qe])|vat)|f)?)|ybj(?:\\ wbof?|\\-wbof?|wbof?))|p(?:bpx(?:\\ fhpx(?:ref?|vat)|\\-fhpx(?:ref?|vat)|fhpx(?:ref?|vat))|enc(?:c(?:r(?:ef|[eq])|vat|l)|f)?|h(?:agf?|z(?:vat|zvat|f)))|qvpx(?:\\ urnq|\\-urnq|rq|urnq|vat|yrff|f)|s(?:hpx(?:rq|vat|f)?|neg(?:r[eq]|vat|[fl])?|rygpu(?:r(?:ef|[efq])|vat)?)|un(?:eq[\\-\\ ]?ba|ys(?:\\ n[fe]|\\-n[fe]|n[fe])frq)|z(?:bgure(?:\\ shpx(?:ref?|vat)|\\-shpx(?:ref?|vat)|shpx(?:ref?|vat))|hgu(?:n(?:\\ shpx(?:ref?|vat|[nnn])|\\-shpx(?:ref?|vat|[nnn])|shpx(?:ref?|vat|[nnn]))|re(?:\\ shpx(?:ref?|vat)|\\-shpx(?:ref?|vat)|shpx(?:ref?|vat)))|reqr?)|temuxl'

TRAN_FROM = '{}{}'.format(
    ''.join([chr(x) for x in range(ord('A'), ord('Z')+1)]),
    ''.join([chr(x) for x in range(ord('a'), ord('z')+1)]))

TRAN_TO = '{}{}{}{}'.format(
    ''.join([chr(x) for x in range(ord('N'), ord('Z')+1)]),
    ''.join([chr(x) for x in range(ord('A'), ord('M')+1)]),
    ''.join([chr(x) for x in range(ord('n'), ord('z')+1)]),
    ''.join([chr(x) for x in range(ord('a'), ord('m')+1)]))

make_trans = getattr(string, 'maketrans', getattr(str, 'maketrans', None)) # py2-3

def decode_regex(regex):
    """
    So we don't have to corrupt our eyes with horrible words
    This is straight from Regexp::Common in perl
    """
    decode_tran = make_trans(TRAN_FROM, TRAN_TO)
    return regex.translate(decode_tran)

def get_blockword_regex():
    sources = [PROFANITY_REGEX_ROT]
    sources.append('sebbo|fulfgre|uvgyre|fu\\vg|qnza|\\ouryy\\o|ulzvr|xvxr|avttre|fulybpx|urro|\\ouror|\\olvq\\o|\\oarteb|\\oavten|c\\vff|phag|pbpxfhpxre|g\\vgf|o\\vgpu|fbebf|furral|furravr|wrj(?!r)|shpx')
    raw_regex = decode_regex('({})'.format('|'.join(sources)))
    # some fixes:
    raw_regex = re.sub(r'ng\b', r'ng?', raw_regex)  # blahing, add blahin'
    # make all 'it' (e.g. sh*t) change to \it to avoid word-joins
    raw_regex = re.sub(r'\\i', r'[i]', raw_regex)
    # Now we attack any non-alphacharacter patterns like s-h-i-z, etc.
    insert_pattern = r"[^a-zA-Z']{0,3}"
    full_regex = re.sub(r'(?<!\\)(\w)(\w)',
                        r'\1{insert}\2{insert}'.format(insert=insert_pattern),
                        raw_regex)
    return full_regex

print(get_blockword_regex())
