"""Public fixtures only: rejection boundaries, bit targets and UI routing."""
import unittest
from unittest.mock import patch
import itertools
import main as app
import password_tools as p
from test_ui import FakeUI
class PasswordTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.wl,cls.dw,_=app.check_core();cls.short=p.load_short(app.UPSTREAM/'eff_short_wordlist_1.txt')
 def test_complete_small_spaces_are_uniform(self):
  for base,count in ((2,1),(3,2),(5,2),(7,1),(11,2)):
   n,space,limit=p.roll_plan(base,count);seen={};reject=0
   for rolls in itertools.product(range(1,7),repeat=n):
    result=p.decode_block(rolls,base,count)
    if result is None:reject+=1
    else:seen[tuple(result)]=seen.get(tuple(result),0)+1
   self.assertEqual(len(seen),space)
   self.assertEqual(set(seen.values()),{limit//space})
   self.assertEqual(reject,6**n-limit)
 def test_strength_and_boundary_all_formats(self):
  for base in (10,26,52,62,85,1296,2048,7776):
   for bits in p.STRENGTHS:
    count=p.choice_count(base,bits);n,space,limit=p.roll_plan(base,count)
    self.assertGreaterEqual(space,1<<bits)
    self.assertLess(base**(count-1),1<<bits)
    for x in (0,limit-1):
     result=p.decode_block(app.core.encode_base6(x,n),base,count)
     self.assertEqual(len(result),count)
     value=0
     for digit in result:value=value*base+digit
     self.assertEqual(value,x%space)
    if limit<6**n:self.assertIsNone(p.decode_block(app.core.encode_base6(limit,n),base,count))
 def test_invalid_input(self):
  n,_,_=p.roll_plan(85,10)
  for rolls in ([1]*(n-1),[7]*n,[True]*n,['1']*n):
   with self.assertRaises(ValueError):p.decode_block(rolls,85,10)
 def test_short_wordlist_order_and_tamper(self):
  self.assertEqual(self.short[0],'acid');self.assertEqual(self.short[-1],'zoom')
  with patch.object(p,'SHORT_HASH','0'*64):
   with self.assertRaises(ValueError):p.load_short(app.UPSTREAM/'eff_short_wordlist_1.txt')
 def test_separators_and_bip39_password_is_not_mnemonic(self):
  self.assertEqual(p.format_words(['abandon','ability'],'Space'),'abandon ability')
  self.assertEqual(p.format_words(['abandon','ability'],'.'),'abandon.ability')
  self.assertEqual(p.format_words(['abandon','ability'],'Capitalise'),'AbandonAbility')
  with self.assertRaises(ValueError):p.format_words(['some','thing'],'None')
  self.assertEqual(p.choice_count(2048,64),6) # password words, no BIP39 checksum added
 def test_password_routes_all_types_strengths(self):
  for kind in (0,2):
   for strength in range(3):
    a=app.App(FakeUI());a.wl=self.wl;a.dw=self.dw
    choices=iter([kind]+([4] if kind==0 else [])+[strength]+([2] if kind==2 else [])+[0])
    a.menu=lambda *args:next(choices);a.note=lambda *args:None
    a.collect=lambda n:([1,2,3,4,5,6]*100)[:n]
    shown=[];verified=[];wordlists=[]
    a.text_result=lambda text,**kwargs:shown.append(text)
    a.display_words=lambda words,*args:wordlists.append(list(words))
    a.verify_copy=lambda words,*args:verified.append(list(words))
    a.confirm_string=lambda text,*args:verified.append(text)
    original=p.decode_block;calls=[]
    def accepted(rolls,base,count):
     calls.append((base,count));return original([1]*len(rolls),base,count)
    with patch.object(app,'require_offline'),patch.object(app.core,'analizza_distribuzione_lanci',return_value=(True,20)),patch.object(p,'decode_block',side_effect=accepted):a.password_menu()
    self.assertEqual(len(shown),1);self.assertEqual(len(verified),1)
    self.assertGreaterEqual(calls[0][0]**calls[0][1],1<<p.STRENGTHS[strength])
    if kind==2:self.assertEqual(shown[0],' '.join(wordlists[0]))
 def test_all_new_flows_reject_offline_failure(self):
  a=app.App(FakeUI());a.wl=self.wl;a.menu=lambda title,options: 2 if title=='Tipo password' else (2 if title=='Separatore' else 0);a.note=lambda *args:None
  a.collect=lambda *args:self.fail('must stop before dice collection')
  with patch.object(app,'require_offline',side_effect=RuntimeError('offline')):
   with self.assertRaises(RuntimeError):a.password_menu()
 def test_secret_text_pages_preserve_wide_characters_and_spaces(self):
  text='W'*45+' '*2+'~'*30
  a=app.App(FakeUI(['OK']*100));a.text_result(text)
  chunks=[line for _,lines,_ in a.ui.frames for line in lines]
  self.assertEqual(''.join(chunks),text)
  self.assertTrue(all(app.body_font().getlength(line)<=app.CANVAS_WIDTH-18 for line in chunks))
 def test_dice_grid_moves_and_undo(self):
  a=app.App(FakeUI(['DOWN','RIGHT','OK','K1','DOWN','LEFT','OK','OK','OK']))
  self.assertEqual(a.collect(2),[6,1])
 def test_home_navigation(self):
  ui=FakeUI(['RIGHT','OK']);ui.home=lambda index:None
  self.assertEqual(app.App(ui).home(),1)
if __name__=='__main__':unittest.main(verbosity=2)
