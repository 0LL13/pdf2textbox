import io
import os

from src.pdf2textbox.pdf2textbox import _get_pdf_file
from src.pdf2textbox.pdf2textbox import _get_textbox
from src.pdf2textbox.pdf2textbox import _extract_textboxes


base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'

# Fragezeichen, Ausrufezeichen, 18.400, Dr., 8. Februar
url1 = '{}Id=MMP16%2F139|14617|14630'.format(base)

# zahlreiche Unterbrechungen, ein einzelnes Wort ("immer") ohne Kontext
url2 = '{}Id=MMP16%2F140|14760|14768'.format(base)

# linke Spalte und rechte Spalte nicht auf der gleichen Höhe
# --> Abruszat's Rede rechte Spalte mit Sätzen aus linker Spalte
url3 = '{}Id=MMP15%2F57|5694|5696'.format(base)

# Zwei Nachnamen, ein Zitat - verliert einen Absatz (des Vorredners)
url4 = '{}Id=MMP16%2F8|368|369'.format(base)


def test_url(url=url1):
    '''test type textbox is dict'''

    pdf = _get_pdf_file(url)
    textbox = _get_textbox(pdf)
    abel_url1 = dict()
    abel_url1[36] = dict()
    abel_url1[37] = dict()
    abel_url1[38] = dict()

    abel_url1[36]['right_column'] = [" 'des  Personalabbaus  eingeholt  werden.  Das  ist  Ihr \\nProblem. \\n'>>",
        " '(Beifall von der SPD) \\n'>>",
        " 'Dass Sie das schmerzt, kann ich menschlich verste-\\nhen. Mein Verständnis endet aber da, wo Sie, obwohl \\nder  Sachverhalt  klar  ist,  immer  wieder  die  gleiche \\nLeier spielen – allein in dieser Plenarrunde dreimal! \\nDas ist, als würden Sie ein totes Pferd reiten. Lassen \\nSie es, es lohnt nicht. – Danke schön. \\n'>>",
        " '(Beifall  von  der  SPD  –  Vereinzelt  Beifall  von \\nden GRÜNEN) \\n'>>",
        " 'Vizepräsident  Oliver  Keymis:  Vielen  Dank,  Frau \\nGebhard. – Für die Fraktion Bündnis 90/Die Grünen \\nspricht nun Herr Abel. \\n'>>",
        " 'Martin-Sebastian  Abel  (GRÜNE):  Herr  Präsident! \\nMeine sehr geehrten Damen und Herren! Lieber Kol-\\nlege Dr. Optendrenk, ich kann es mir nicht ersparen: \\nMit diesem Tiefgang können Sie auf der Düssel se-\\ngeln gehen. Es ist nicht auszuhalten, wie Sie diesen \\nStrohhalm, der Ihnen bei dem Thema Haushalt und \\nFinanzen einzig übrig bleibt, überstrapazieren. Er ist \\neigentlich schon bei Ihrer Rede abgeknickt, Herr Kol-\\nlege. \\n'>>",
        " '(Beifall von den GRÜNEN) \\n'>>",
        " 'Ich  will  Ihnen  das  mit  den  Soll-  und  Ist-Zahlen  von \\n2013,  2014,  2015  und  2016  deutlich  machen.  Wir \\nhatten 2013 und 2014 – zwischen Soll und Ist – eine \\nStellenbesetzung  von  97,6 %. Wir  hatten  2014 und \\n2015 eine Stellenbesetzung von 98,1 %. Wir hatten \\neinen leichten Rückgang 2016 und 2017 und sind bei \\neiner Stellenbesetzung von 96,6 %. \\n'>>",
        " 'Man  darf  daran  erinnern,  wie  viele  Nachtragshaus-\\nhalte wir auf den Weg gebracht haben und was die \\nHerausforderungen in den Jahren waren. Wir haben \\nüber  4  Milliarden €  an  Landesgeld  bewegt  in  noch \\nnicht einmal einem Haushaltsjahr. Dass die gesam-\\nten – einschließlich der zusätzlichen – Stellen, die im \\nSystem  sind,  trotzdem  zu  96,6 %  besetzt  worden \\nsind,  ist  ein  großer  Erfolg.  Das  kann  uns  dennoch \\nnicht zufriedenstellen, weil wir die Stellen, die wir als \\nHaushaltsgesetzgeber  in  den  Haushalt  einstellen \\nund mit Geld hinterlegen, auch besetzen wollen.  \\n'>>",
        " 'Von Ihnen haben wir dabei immer die Kritik gehört, \\ndass  das  zu  viel  sei.  In  den  Ausschüssen  sind  Sie \\neine Doppelstrategie gefahren, als Sie sagten, Quan-\\ntität  sei  nicht  gleich  Qualität.  Man  verbessere  nicht \\nunbedingt das System Schule, nur indem man Leh-\\nrerinnen und Lehrer einstellt. Das alles ist in den zahl-\\nreichen  Protokollen,  die  Herr  Witzel  beantragt  hat, \\nWort für Wort nachzulesen. Hören Sie doch auf, so \\nzu tun und sich hier so hinzustellen! \\n'>>",
        " '(Vereinzelt Beifall von den GRÜNEN) \\n'>>"]

    abel_url1[37]['header'] = [" 'Landtag  \\nNordrhein-Westfalen \\n'>>", " ' \\n'>>", " '14623 \\n'>>", " '16.03.2017 \\nPlenarprotokoll 16/139 \\n'>>", '0>>']

    abel_url1[37]['left_column'] = [" 'Da darf man auch an Ihre Zeit erinnern. Sie tun im-\\nmer  so:  Ach,  das  ist  sieben  Jahre  her.  –  Ja,  aber \\n2005 bis 2010 haben Sie über alle Ressorts hinweg \\n1,5 % Personal abgebaut. \\n'>>",
    " '(Zuruf von Ralf Witzel [FDP]) \\n'>>",
    " 'Sie  haben  uns  Lücken  hinterlassen.  Sie  reden  von \\nder Demografie bei der Polizei. Sie haben sich noch \\nnicht einmal getraut, den Demografiebericht zu ver-\\nöffentlichen, meine Damen und Herren. \\n'>>",
    " '(Beifall von den GRÜNEN) \\n'>>",
    " 'Dieses Bundesland hat, von 2013 angefangen, lange \\nJahre  als  einziges  Bundesland  mehr  Polizistinnen \\nund Polizisten eingestellt, als in den Ruhestand gin-\\ngen.  Alle  anderen  Bundesländer  haben  gekürzt, \\nauch  die  Innenminister  aus  den  neuen  Bundeslän-\\ndern, die alle von der CDU sind, mit der Konsequenz, \\ndass wir hier eine Reihe von Bereitschaften hatten, \\ndie an den Wochenenden nur in den neuen Bundes-\\nländern in den Stiefeln standen. Dann haben Sie uns \\nhier  in  den  Haushaltsdebatten  diese  Länder  auch \\nnoch als glänzendes Vorbild dargestellt. So einfach \\ngeht  es  nicht,  meine  lieben  Kolleginnen  und  Kolle-\\ngen. \\n'>>",
    " '(Beifall von den GRÜNEN) \\n'>>",
    " 'Vizepräsident  Oliver  Keymis:  Herr  Kollege  Abel, \\ngestatten Sie eine Zwischenfrage von Herrn Lohn? \\n'>>",
    " 'Martin-Sebastian Abel (GRÜNE): Ja, sehr gern. \\n'>>",
    " 'Vizepräsident  Oliver  Keymis:  Bitte  schön,  Herr \\nLohn. \\n'>>",
    " 'Werner Lohn (CDU): Vielen Dank, Herr Kollege A-\\nbel. Sie haben gerade Ausführungen zu den Einstel-\\nlungszahlen und zu der Personalentwicklung im Be-\\nreich Polizei gemacht. \\n'>>",
    " 'Sind Sie bereit, zur Kenntnis zu nehmen, dass es die \\nrot-grüne Regierung war, die in den Jahren 2004 und \\n2005  die  Einstellungszahlen  von  1.100  auf  faktisch \\n480 mehr als halbiert hat und damit im Prinzip die Ur-\\nsache dafür gelegt hat, dass wir alles wiedergutma-\\nchen mussten? \\n'>>",
    " '(Beifall  von  Christian Möbius [CDU]  – Zurufe \\nvon den GRÜNEN) \\n'>>",
    " 'Martin-Sebastian  Abel  (GRÜNE):  Herr  Kollege \\nLohn, ja, ich bin bereit, das zur Kenntnis zu nehmen, \\nwenn  Sie  gleichzeitig  bereit  sind,  zur  Kenntnis  zu \\nnehmen, dass Sie dann fünf Jahre Zeit gehabt hät-\\nten, diese Zahlen wieder anzuheben. \\n'>>",
    " '(Ralf Witzel [FDP]: Verdoppelt!) \\n'>>", " ' \\n'>>"]
    abel_url1[37]['right_column'] = [" '– Diese Verdoppelung führte aber zu einem negati-\\nven Ist. Die Verdoppelung führte im Vergleich zu den \\nPensionen  dazu,  dass  die  Polizei  Stellen  verloren \\nhatte  und  dass  wir  nicht  genügend  Polizeibeamtin-\\nnen und Polizeibeamte im Vollzug hatten. Das gehört \\ndoch auch zur Wahrheit dazu. \\n'>>",
    " 'Zur Wahrheit gehört ebenfalls, dass wir die höchsten \\nEinstellungszahlen  bei  der  Polizei  in  Nordrhein-\\nWestfalen in der Geschichte dieses Landes haben. \\n'>>",
    " '(Beifall  von  den  GRÜNEN  –  Zuruf  von  Ralf \\nWitzel [FDP]) \\n'>>",
    " 'Wir haben doch erst vorgestern über Mehrforderun-\\ngen gesprochen. Es sind sich doch nicht einmal die \\nGewerkschaften  einig,  ob  wir  überhaupt  genügend \\nAusbildungskapazitäten haben, um noch mehr aus-\\nbilden zu können. Das heißt: Wir gehen da schon an \\ndas  Limit.  Das  kann  man  doch  jetzt  nicht  wegwi-\\nschen, dass wir aufgestockt haben. Polizisten wach-\\nsen nicht an Bäumen, Lehrerinnen und Lehrer auch \\nnicht. Wir  müssen  da  ausbilden.  Das,  was  Sie  fünf \\nJahre  verpennt  haben,  mussten  wir  aufholen,  und \\ndas haben wir aufgeholt. \\n'>>",
    " '(Zuruf von Ralf Witzel [FDP]: Unverschämt!) \\n'>>",
    " 'Jedes  Mal  haben  Sie  sich  in  der  Haushaltsdebatte \\nhier hingestellt und die Neuverschuldung und die zu-\\nsätzlichen Stellen angeprangert.  \\n'>>",
    " 'Herr Witzel, wenn Sie hier am lautesten dazwischen-\\nbrüllen,  sage  ich:  immer  dieses  Herumhacken  auf \\nder  Umweltverwaltung!  Gehen  Sie  doch  einmal  zu \\nVeranstaltungen,  wie  zum  Beispiel  letzte  Woche  in \\nEssen  zum  Informationstreffen  für  Tierschutzbeauf-\\ntragte und Tierexperimentatoren, und hören Sie sich \\ndoch von der Wissenschaft und der Industrie das Lob \\nan  diese  Landesregierung  an,  dass  endlich  beim \\nLANUV Stellen geschaffen werden, um die Bearbei-\\ntungszeiten zu verkürzen. Das ist für viele Unterneh-\\nmen hier standortentscheidend. Sie geißeln das als \\nUmweltbürokratie. \\n'>>",
    " '(Beifall von den GRÜNEN und der SPD) \\n'>>",
    " 'Was Sie fordern, ist wirtschaftsfeindlich, Herr Witzel! \\n'>>",
    " '(Zuruf von Ralf Witzel [FDP]) \\n'>>",
    " '18.400 Stellen zusätzlich im System Schule. Der Zu-\\nwachs, den wir im Bereich Schule haben, ist, gemes-\\nsen  an  dem  Zuwachs,  den  Sie  zweifelsohne  zwi-\\nschen 2005 und 2010 hatten – eine Milliarde Haus-\\nhaltsmittel  und  1.000  zusätzliche  Stellen  –,  viermal \\nmehr  Aufwuchs.  Im  Vergleich  zu  2010  haben  wir \\n18.400 zusätzliche Stellen im System Schule.  \\n'>>", " 'Wir haben – das haben wir schon gesagt – in NRW \\nmehr Polizei eingestellt, als es die anderen Bundes-\\nländer und der Bund getan haben. Der Bund hat bei \\nder Bundespolizei auch gespart.  \\n'>>", " 'Wir  haben  unsere  Finanzverwaltung  gestärkt.  Wir \\nhaben mit dem jüngsten Haushalt erreicht, dass trotz \\n'>>"]

    abel_url1[38]['header'] = [" 'Landtag  \\nNordrhein-Westfalen \\n'>>", " ' \\n'>>", " '14624 \\n'>>", " '16.03.2017 \\nPlenarprotokoll 16/139 \\n'>>", '0>>']

    abel_url1[38]['left_column'] = [" 'mangelnder Umsetzung, die bei der Kfz-Steuer und \\nbei den Zollverwaltungsämtern vor allen Dingen am \\nBund lag, die Finanzverwaltung einen Teil der Stellen \\nbehalten  darf.  Wir  haben  1.100  Stellen  im  Saldo \\nmehr  bei  der  Finanzverwaltung.  Wir  haben  42 % \\nmehr Betriebsprüferinnen und -prüfer, die für Steuer-\\ngerechtigkeit sorgen und die dafür sorgen, dass die \\nEinnahmen,  mit  denen  wir  wichtige  Zukunftsaufga-\\nben finanzieren, hereinkommen.  \\n'>>",
            " 'Dazu kann ich Ihnen wirklich nur sagen: Sie müssen \\nsich schon entscheiden. Erinnern Sie sich doch ein-\\nmal an die Debatte zum Haushalt 2015/2016, als sich \\nHerr Laschet hier hingestellt und ernsthaft gefordert \\nhat – das ist alles dokumentiert und nachzulesen –, \\ndass  wir  wie  das  Saarland  vorgehen  sollen.  Er  hat \\n10 % der Stellen im öffentlichen Dienst zur Disposi-\\ntion gestellt.  \\n'>>",
            " 'Ich  habe  das  noch  einmal  auf  Ihrer  Webseite  ge-\\nsucht, meine Damen und Herren von der CDU. Ko-\\nmischerweise  ist  dieses  Haushaltskonzept  nicht \\nmehr zu finden. Ich habe nur noch eine Kopie davon. \\nMeine ernsthafte Bitte an Sie: Ich würde mich freuen, \\nwenn Sie uns dieses Haushaltskonzept noch einmal \\nzustellen könnten. Wenn Sie es nicht tun, ist es auch \\ngut, dann kann ich das wenigstens sagen. Aber die-\\nsen  Zick-zack-Kurs,  diese  Doppelstrategie,  die  Sie \\nhier über Jahre durchgezogen haben, in den Haus-\\nhaltsdebatten immer die Sparer und  die  Mahner  zu \\ngeben, aber in jedem einzelnen Fachausschuss und \\nmit Kleinen Anfragen in jedem Bereich zu suggerie-\\nren, wir würden nicht genügend Personal einstellen, \\ndas haben die Leute wirklich durchschaut. Mit dieser \\nTaktik offenbaren Sie eigentlich nur, wie verzweifelt \\nSie sind, weil die Zahlen eben stimmen, meine Da-\\nmen und Herren.  \\n'>>",
            " 'Das alles haben Sie hier in den Raum gestellt trotz \\nanderer Zahlen, die wir zwischenzeitlich von der Lan-\\ndesregierung  bekommen  haben,  und  obwohl  die \\nMaßnahmen  der  Schulministerin  bereits  greifen. \\nDass die Schulministerin heute übrigens bei der Kul-\\ntusministerkonferenz ist, ist allen Parlamentarischen \\nGeschäftsführern hier im Raum bekannt. Deswegen \\nfinde ich diesen Anwurf, der eben kam, nicht in Ord-\\nnung. Die Bildungsministerin ist bei der KMK, und sie \\nhat  am  8. Februar  im  Schulausschuss  genau  die \\nMaßnahmen aufgelistet, die im Bereich Schule jetzt \\ngreifen.  \\n'>>",
            " 'Wenn das alles ist, was von der Opposition kommt, \\nfrage  ich  Sie:  Was  wollen  Sie  denn  eigentlich  ma-\\nchen?  Wo  waren  denn  Ihre  Haushaltsanträge  für \\nmehr  Personal? Wo  waren denn  Ihre  Haushaltsan-\\nträge,  um  die  Ausbildungskapazitäten  zu  erhöhen? \\nWenn  Sie  dazu  in  die  Historie  schauen,  finden  Sie \\ndazu nichts. Es gibt keine Anträge von Ihnen. Wenn \\nSie  ernsthaft  den  Anspruch  haben,  Verantwortung \\nfür  dieses  Land  zu  übernehmen,  kommen  Sie  mit \\ndiesem  Tiefgang  nicht  voran.  Das  ist  weder  redlich \\n \\n'>>"]

    abel_url1[38]['right_column'] = [" 'noch  bringt  es  das  Land  irgendwie  weiter.  –  Vielen \\nDank, meine Damen und Herren.  \\n'>>", " '(Beifall von den GRÜNEN und der SPD) \\n'>>"]

    assert textbox[36]['right_column'] == abel_url1[36]['right_column']
    assert textbox[37]['right_column'] == abel_url1[37]['right_column']
    assert textbox[38]['right_column'][:2] == abel_url1[38]['right_column'][:2]

    assert textbox[37]['left_column'] == abel_url1[37]['left_column']
    assert textbox[38]['left_column'] == abel_url1[38]['left_column']

    assert textbox[37]['header'] == abel_url1[37]['header']
    assert textbox[38]['header'] == abel_url1[38]['header']

