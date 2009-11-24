#!/usr/bin/env python
# encoding: utf-8

# created november 2009 by danielroseman for Hudora GmbH

from xml.etree import cElementTree as ET
xml = ET.XML(r"""<?xml version="1.0" encoding="UTF-8"?>
<WHOLE Date="30/10/2009">
<ENTITY Id="1" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7 (2): 21.2.2002. Head of Government and as such responsible for activities that seriously undermine democracy, respect for human rights and the rule of law.">
<NAME Id="1" Entity_id="1" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<LASTNAME>Mugabe</LASTNAME>
<FIRSTNAME>Robert</FIRSTNAME>
<MIDDLENAME>Gabriel</MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>President</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="1" Entity_id="1" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1924-02-21</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
<PASSPORT Id="315" Entity_id="1" legal_basis="77/2009 (OJ L 23)" reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE">
<NUMBER>AD001095</NUMBER>
<COUNTRY></COUNTRY>
</PASSPORT>
</ENTITY>
<ENTITY Id="2" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7 (2): 25.7.2002. Former member of the Government and as such engaged in activities that seriously undermine democracy, respect for human rights and the rule of law.">
<NAME Id="2" Entity_id="2" legal_basis="777/2007 (OJ L 173)" reg_date="2007-07-03" pdf_link="http://eur-lex.europa.eu/LexUriServ/site/en/oj/2007/l_173/l_17320070703en00030015.pdf" programme="ZWE">
<LASTNAME>Buka</LASTNAME>
<FIRSTNAME>Flora</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>F</GENDER>
<TITLE></TITLE>
<FUNCTION>President’s office and former Minister of State for Special Affairs responsible for Land and Resettlement Programmes</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="2572" Entity_id="2" legal_basis="777/2007 (OJ L 173)" reg_date="2007-07-03" pdf_link="http://eur-lex.europa.eu/LexUriServ/site/en/oj/2007/l_173/l_17320070703en00030015.pdf" programme="ZWE">
<LASTNAME>Buka</LASTNAME>
<FIRSTNAME>Flora</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>F</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Minister of State in the Vice-President’s office</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="5715" Entity_id="2" legal_basis="777/2007 (OJ L 173)" reg_date="2007-07-03" pdf_link="http://eur-lex.europa.eu/LexUriServ/site/en/oj/2007/l_173/l_17320070703en00030015.pdf" programme="ZWE">
<LASTNAME>Buka</LASTNAME>
<FIRSTNAME>Flora</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>F</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Minister of State for the Land Reform in the President's Office</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="5716" Entity_id="2" legal_basis="777/2007 (OJ L 173)" reg_date="2007-07-03" pdf_link="http://eur-lex.europa.eu/LexUriServ/site/en/oj/2007/l_173/l_17320070703en00030015.pdf" programme="ZWE">
<LASTNAME>Bhuka</LASTNAME>
<FIRSTNAME>Flora</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>F</GENDER>
<TITLE></TITLE>
<FUNCTION></FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="2" Entity_id="2" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1968-02-25</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="3" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7 (2): 21.2.2002. Member of the Government and as such engaged in activities that seriously undermine democracy, respect for human rights and the rule of law.">
<NAME Id="4" Entity_id="3" legal_basis="314/2004 (OJ L 55)" reg_date="2004-02-21" pdf_link="http://eur-lex.europa.eu/pri/en/oj/dat/2004/l_055/l_05520040224en00010013.pdf" programme="ZWE">
<LASTNAME>Charamba</LASTNAME>
<FIRSTNAME>George</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Permanent Secretary Department for Information and Publicity</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="462" Entity_id="3" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1963-04-04</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
<PASSPORT Id="322" Entity_id="3" legal_basis="77/2009 (OJ L 23)" reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE">
<NUMBER>AD002226</NUMBER>
<COUNTRY></COUNTRY>
</PASSPORT>
</ENTITY>
<ENTITY Id="4" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7 (2): 14.9.2002. Former member of the Government with ongoing ties.">
<NAME Id="5" Entity_id="4" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<LASTNAME>Charumbira</LASTNAME>
<FIRSTNAME>Fortune</FIRSTNAME>
<MIDDLENAME>Zefanaya</MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Deputy Minister for Local Government, Public Works and National Housing</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="3" Entity_id="4" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1962-06-10</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="5" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7 (2): 25.7.2002. Former member of the Government and as such engaged in activities that seriously undermine democracy, respect for human rights and the rule of law.">
<NAME Id="7" Entity_id="5" legal_basis="77/2009 (OJ L 23)" reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE">
<LASTNAME>Chigwedere</LASTNAME>
<FIRSTNAME>Aeneas</FIRSTNAME>
<MIDDLENAME>Soko</MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Provincial Governor: Mashonaland East</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="4" Entity_id="5" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1939-11-25</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="6" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7 (2): 21.2.2002. Member of the security forces and bearing wide responsibility for serious violations of the freedom of peaceful assembly.">
<NAME Id="9" Entity_id="6" legal_basis="77/2009 (OJ L 23)" reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE">
<LASTNAME>Chihuri</LASTNAME>
<FIRSTNAME>Augustine</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER></GENDER>
<TITLE></TITLE>
<FUNCTION>Police Commissioner</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="5" Entity_id="6" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1953-03-10</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="8" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7(2): 21.2.2002. Member of the Government and as such engaged in activities that seriously undermine democracy, respect for human rights and the rule of law.">
<NAME Id="2575" Entity_id="8" legal_basis="314/2004 (OJ L 55)" reg_date="2004-02-21" pdf_link="http://eur-lex.europa.eu/pri/en/oj/dat/2004/l_055/l_05520040224en00010013.pdf" programme="ZWE">
<LASTNAME>Chinamasa</LASTNAME>
<FIRSTNAME>Patrick</FIRSTNAME>
<MIDDLENAME>Anthony</MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Minister of Justice, Legal and Parliamentary Affairs</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="7" Entity_id="8" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1947-01-25</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="9" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7(2): 25.7.2002. Former member of the Government with ongoing ties to the Government.">
<NAME Id="12" Entity_id="9" legal_basis="777/2007 (OJ L 173)" reg_date="2007-07-03" pdf_link="http://eur-lex.europa.eu/LexUriServ/site/en/oj/2007/l_173/l_17320070703en00030015.pdf" programme="ZWE">
<LASTNAME>Chindori-Chininga</LASTNAME>
<FIRSTNAME>Edward</FIRSTNAME>
<MIDDLENAME>Takaruza</MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Minister of Mines and Mining Development</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="8" Entity_id="9" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1955-03-14</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="10" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7(2): 21.2.2002. Member of the security forces and complicit in forming or directing repressive state policy.">
<NAME Id="13" Entity_id="10" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<LASTNAME>Chiwenga</LASTNAME>
<FIRSTNAME>Constantine</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE>General</TITLE>
<FUNCTION>Commander Zimbabwe Defence Forces</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="2577" Entity_id="10" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<LASTNAME>Chiwenga</LASTNAME>
<FIRSTNAME>Constantine</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Army Commander, Lieutenant General</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="9" Entity_id="10" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1956-08-25</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="11" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7(2): 21.2.2002. Former member of the Government with ongoing ties and bearing wide responsibility for serious violations of human rights.">
<NAME Id="14" Entity_id="11" legal_basis="77/2009 (OJ L 23)" reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE">
<LASTNAME>Chiwewe</LASTNAME>
<FIRSTNAME>Willard</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Provincial Governor: Masvingo</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="5719" Entity_id="11" legal_basis="777/2007 (OJ L 173)" reg_date="2007-07-03" pdf_link="http://eur-lex.europa.eu/LexUriServ/site/en/oj/2007/l_173/l_17320070703en00030015.pdf" programme="ZWE">
<LASTNAME>Chiwewe</LASTNAME>
<FIRSTNAME>Willard</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Senior Secretary responsible for Special Affairs in the President's Office</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="10" Entity_id="11" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1949-03-19</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="12" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7(2): 21.2.2002. Member of the Government and as such engaged in activities that seriously undermine democracy, respect for human rights and the rule of law.">
<NAME Id="15" Entity_id="12" legal_basis="236/2007 (OJ L 66)" reg_date="2007-03-06" pdf_link="http://eur-lex.europa.eu/LexUriServ/site/en/oj/2007/l_066/l_06620070306en00140016.pdf" programme="ZWE">
<LASTNAME>Chombo</LASTNAME>
<FIRSTNAME>Ignatius</FIRSTNAME>
<MIDDLENAME>Morgan Chininya</MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Minister of Local Government, Public Works and Urban Development</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<BIRTH Id="11" Entity_id="12" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1952-08-01</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
<ENTITY Id="13" Type="P" legal_basis="1210/2003 (OJ L 169)"  reg_date="2003-07-09" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2003:169:0006:0023:EN:PDF" programme="IRQ"  remark="UNSC RESOLUTION 1483">
<NAME Id="17" Entity_id="13" legal_basis="1210/2003 (OJ L 169)" reg_date="2003-07-09" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2003:169:0006:0023:EN:PDF" programme="IRQ">
<LASTNAME>Hussein Al-Tikriti</LASTNAME>
<FIRSTNAME>Saddam</FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION></FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="19" Entity_id="13" legal_basis="1210/2003 (OJ L 169)" reg_date="2003-07-09" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2003:169:0006:0023:EN:PDF" programme="IRQ">
<LASTNAME></LASTNAME>
<FIRSTNAME></FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME>Abu Ali</WHOLENAME>
<GENDER></GENDER>
<TITLE></TITLE>
<FUNCTION></FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="380" Entity_id="13" legal_basis="1210/2003 (OJ L 169)" reg_date="2003-07-09" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2003:169:0006:0023:EN:PDF" programme="IRQ">
<LASTNAME></LASTNAME>
<FIRSTNAME></FIRSTNAME>
<MIDDLENAME></MIDDLENAME>
<WHOLENAME>Abou Ali</WHOLENAME>
<GENDER></GENDER>
<TITLE></TITLE>
<FUNCTION></FUNCTION>
<LANGUAGE>FR</LANGUAGE>
</NAME>
<BIRTH Id="14" Entity_id="13" legal_basis="1210/2003 (OJ L 169)" reg_date="2003-07-09" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2003:169:0006:0023:EN:PDF" programme="IRQ">
<DATE>28 April 1937</DATE>
<PLACE>al-Awja, near Tikrit</PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
<BIRTH Id="158" Entity_id="13" legal_basis="1210/2003 (OJ L 169)" reg_date="2003-07-09" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2003:169:0006:0023:EN:PDF" programme="IRQ">
<DATE></DATE>
<PLACE>Al-Awja, near Tikrit (J.O. ES)</PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
<CITIZEN Id="1" Entity_id="13" legal_basis="1210/2003 (OJ L 169)" reg_date="2003-07-09" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2003:169:0006:0023:EN:PDF" programme="IRQ">
<COUNTRY>IRQ</COUNTRY>
</CITIZEN>
</ENTITY>
<ENTITY Id="66" Type="P" legal_basis="77/2009 (OJ L 23)"  reg_date="2009-01-27" pdf_link="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF" programme="ZWE"  remark="Date of designation referred to in Article 7(2): 21.2.2002. Member of the Government and as such engaged in activities that seriously undermine democracy, respect for human rights and the rule of law.">
<NAME Id="98" Entity_id="66" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<LASTNAME>Mudenge</LASTNAME>
<FIRSTNAME>Isack</FIRSTNAME>
<MIDDLENAME>Stanilaus Gorerazvo</MIDDLENAME>
<WHOLENAME>Testy TestName</WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Former Minister of Foreign Affairs</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<NAME Id="4137" Entity_id="66" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<LASTNAME>Mudenge</LASTNAME>
<FIRSTNAME>Isack</FIRSTNAME>
<MIDDLENAME>Stanilaus Gorerazvo</MIDDLENAME>
<WHOLENAME></WHOLENAME>
<GENDER>M</GENDER>
<TITLE></TITLE>
<FUNCTION>Minister of Higher Tertiary Education</FUNCTION>
<LANGUAGE></LANGUAGE>
</NAME>
<ADDRESS Id="3" Entity_id="66" legal_basis="1643/2002 (OJ L 247)" reg_date="2002-09-14" pdf_link="http://eur-lex.europa.eu/pri/en/oj/dat/2002/l_247/l_24720020914en00220024.pdf" programme="ZWE">
<NUMBER></NUMBER>
<STREET></STREET>
<ZIPCODE></ZIPCODE>
<CITY></CITY>
<COUNTRY></COUNTRY>
<OTHER></OTHER>
</ADDRESS>
<BIRTH Id="68" Entity_id="66" legal_basis="898/2005 (OJ L 153)" reg_date="2005-06-16" pdf_link="http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf" programme="ZWE">
<DATE>1941-12-17</DATE>
<PLACE></PLACE>
<COUNTRY></COUNTRY>
</BIRTH>
</ENTITY>
</WHOLE>""")