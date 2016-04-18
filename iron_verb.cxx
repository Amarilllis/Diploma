#encoding "utf8"
#GRAMMAR_ROOT S
Vb_left -> Verb<rt> Noun<kwtype='характеристики'>;
Vb_right -> Noun<kwtype='характеристики'> Verb<rt>;
S -> Vb_right | Vb_left;