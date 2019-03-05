import os
import shutil

import pytest


@pytest.fixture(scope='session')
def out_dir():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(tests_dir, 'out')
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    return out_dir


@pytest.fixture(scope="session")
def lorem_ipsums():
    return [
        """\
Lorem ipsum dolor sit amet, an homero graece sapientem cum, nam ullum etiam ubique ei.
Vim id fugit menandri, et has vivendo partiendo liberavisse, cu unum justo assum sed.
Qui ut facer discere facilisis, sea feugait fabellas et, ea sed iuvaret euripidis. Recusabo scribentur
an vim, no semper commune dissentiet vis, duo dico nulla ancillae eu. Quo unum populo et, cum no dicant
dolore suscipiantur.Ferri affert expetenda ei duo, vel cu legimus splendide. Oblique dignissim elaboraret vix cu,
eos errem graeco ponderum ut, id quidam semper melius mei. Tantas munere ornatus an vel.
Sit simul tempor tibique cu.
His te erat etiam phaedrum, qui graece dicunt sensibus te, qui ad salutandi periculis.
At quaeque sensibus sed, persius dolorum usu ea, apeirian urbanitas ius te. Eos doctus
virtute ne, id qui choro possit graeco. Ei duo dolor expetendis scribentur, ut decore
labitur consetetur pri. Summo ludus referrentur cu sit, elitr periculis voluptaria vix ei.
Vix soluta facilis repudiandae ne. Ius graecis fabellas ad, duo percipitur instructior an.
Nec ut veri melius veritus, tincidunt incorrupte est at. Ut vidit ridens postulant eam,
eos ullum saperet et, eam sale tempor ea. Et vis rebum sanctus reprehendunt, ea mei suas liber virtute.
Pericula electram mea ei. Usu at nulla mollis cotidieque, impetus qualisque scriptorem ea usu.
Ius altera doctus cu, cu ius elitr dicant dissentias.""",
        """\
Placerat gloriatur mei ea. Mel id alienum pertinacia, ne per viris choro mnesarchum, ad inani
consul his. Error audiam explicari quo an, mea corpora invenire ex. Id luptatum dissentiet eam.
Utroque adolescens ut pro, te vel labitur iudicabit. Dicant putent tractatos duo in.
An harum postulant persecuti vim. Nec alia eius ut, id vis vide tibique repudiare, facete antiopam
concludaturque ut sit. Eam ridens dicunt ocurreret ad, sumo omnesque scribentur an mel.
Eos graeco alienum cu, vim eius erat et, graeco eirmod et mea. Ex pri viderer corpora, sea deleniti
petentium signiferumque in. Assum scripta ad vim, his possim explicari cu, reprimique eloquentiam at eum.
Ridens laoreet oporteat ex vis, pertinax forensibus ex mei.
Atqui animal utamur ea nam, nam id quodsi ornatus probatus. Lorem nostrud in mei.
Ne mei etiam ignota. Ut dico veritus pri, facilisis corrumpit vis ei.
Est utroque consulatu ne, deleniti perfecto ocurreret id duo. Tibique accusam in mea.
Ex pro delenit persequeris, qui magna maluisset definitionem id.
Has postulant omittantur ad. Per causae mediocrem no, duo ex sumo dicta eirmod. His at nemore explicari.
Est ex suas enim possit, mea corpora gloriatur reprehendunt ex. Mea esse sadipscing omittantur in.
Omittam signiferumque ad nec, in repudiare temporibus mel, pro in suscipit salutatus.
Eam verear omittam omnesque cu, scripta deserunt te mei. Mea an commodo praesent elaboraret.
Id soleat denique phaedrum mea, cu vitae quando pro. Commune perfecto adversarium et duo, scripta
euripidis no nam. Tota eloquentiam ex his, sit no tantas philosophia interpretaris.""",
        """\
Atqui animal utamur ea nam, nam id quodsi ornatus probatus. Lorem nostrud in mei.
Ne mei etiam ignota. Ut dico veritus pri, facilisis corrumpit vis ei.
Est utroque consulatu ne, deleniti perfecto ocurreret id duo. Tibique accusam in mea.
Ex pro delenit persequeris, qui magna maluisset definitionem id.
Has postulant omittantur ad. Per causae mediocrem no, duo ex sumo dicta eirmod. His at nemore explicari.
Est ex suas enim possit, mea corpora gloriatur reprehendunt ex. Mea esse sadipscing omittantur in.
Omittam signiferumque ad nec, in repudiare temporibus mel, pro in suscipit salutatus.
Sed magna oportere ullamcorper cu, noster maiorum vituperata an vim. Eu tamquam commune phaedrum pri,
minim mentitum at ius. Per alterum volumus ex, in per aeterno explicari urbanitas. Modo omnis animal
eum id, laudem vivendo noluisse no nam, sed meis elitr singulis ei. Utinam iudicabit moderatius per ut.
Mundi principes eum ea, velit sapientem theophrastus vel at. Malis facer ad vel, cetero delicata
id usu. Alterum liberavisse ea vis. Mea ignota possim ex, vim sale iusto in. Ferri justo consul
eum ut, usu corpora ocurreret et, mea ut malis dolore viderer.""",
        """\
Mundi principes eum ea, velit sapientem theophrastus vel at. Malis facer ad vel, cetero delicata
id usu. Alterum liberavisse ea vis. Mea ignota possim ex, vim sale iusto in. Ferri justo consul
eum ut, usu corpora ocurreret et, mea ut malis dolore viderer.
Sed magna oportere ullamcorper cu, noster maiorum vituperata an vim. Eu tamquam commune phaedrum pri,
minim mentitum at ius. Per alterum volumus ex, in per aeterno explicari urbanitas. Modo omnis animal
eum id, laudem vivendo noluisse no nam, sed meis elitr singulis ei. Utinam iudicabit moderatius per ut.
Mundi principes eum ea, velit sapientem theophrastus vel at. Malis facer ad vel, cetero delicata
id usu. Alterum liberavisse ea vis. Mea ignota possim ex, vim sale iusto in. Ferri justo consul
eum ut, usu corpora ocurreret et, mea ut malis dolore viderer.
Sed magna oportere ullamcorper cu, noster maiorum vituperata an vim. Eu tamquam commune phaedrum pri,
minim mentitum at ius. Per alterum volumus ex, in per aeterno explicari urbanitas. Modo omnis animal
eum id, laudem vivendo noluisse no nam, sed meis elitr singulis ei. Utinam iudicabit moderatius per ut.
Id salutandi hendrerit posidonium sea, ut utinam consetetur mediocritatem sea. An admodum scaevola mel,
vel equidem qualisque ne. Sit ex mundi argumentum, delenit veritus qui ei. Usu iisque feugait eleifend cu.""",
        """\
Quo error dolor labitur at. Ut mundi dicunt mandamus pro, torquatos cotidieque cu vel. Tale everti
adipiscing vel te, maluisset assentior ea vel. Pri ex appetere pertinax, ut nam lorem legere, ius eu probo
lobortis conceptam. Invidunt molestiae in duo. Admodum convenire expetendis ea sed. Pro ea veri verear persecuti,
rebum saepe nec ei. Per cu feugiat officiis, te nostrum tacimates sapientem usu. Mel soleat quaeque
aliquid te, oratio verterem vel ei. Porro fuisset complectitur id pri.
Quo error dolor labitur at. Ut mundi dicunt mandamus pro, torquatos cotidieque cu vel. Tale everti
adipiscing vel te, maluisset assentior ea vel. Pri ex appetere pertinax, ut nam lorem legere, ius eu probo
lobortis conceptam. Invidunt molestiae in duo. Admodum convenire expetendis ea sed. Pro ea veri verear persecuti,
rebum saepe nec ei. Per cu feugiat officiis, te nostrum tacimates sapientem usu. Mel soleat quaeque
aliquid te, oratio verterem vel ei. Porro fuisset complectitur id pri. Ex mei aliquam ponderum persequeris,
has ex diam argumentum, vim harum diceret interesset ex. Congue euismod ne sed, sit dolor civibus electram
ei, cu sed case offendit euripidis. Cu per illud possim ullamcorper, sit ut vide debet sadipscing, populo
nonumes intellegat mea no. Usu cetero invenire prodesset cu, audiam epicurei ullamcorper duo no. Saepe
tation imperdiet an nec.
"""]
