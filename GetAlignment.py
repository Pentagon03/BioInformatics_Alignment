from pairwise import *
#Modified pairwise2 module - _make_score_matrix_generic
#Local Alignment
s1 = "GGTTGAC" # Vertical
s2 = "TGTTACG" # Horizontal
for a in align.localms(s1, s2,  match=1, mismatch=-1, open=-2, extend=-2, penalize_end_gaps = True, force_generic=True):
    print(format_alignment(*a))

#Global Alignment
s1 = "GGTTGAC" # Vertical
s2 = "TGTTACG" # Horizontal
for a in align.globalms(s1, s2, match=1, mismatch=-1, open=-2, extend=-1, penalize_end_gaps = True, force_generic=True):
    print(format_alignment(*a))