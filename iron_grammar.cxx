#encoding "utf8"
#GRAMMAR_ROOT S

Ad -> (Adj<gnc-agr[1]>) Noun<kwtype='характеристики', rt, gnc-agr[1]>;
Vb -> (Verb<gnc-agr[1]>) Noun<kwtype='характеристики', rt, gnc-agr[1]>;
S -> Ad | Vb;