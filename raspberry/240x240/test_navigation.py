"""Navigation and language regression tests, using public strings only."""
import unittest
from unittest.mock import Mock, patch
import main as app
import i18n
from test_ui import FakeUI
class NavTests(unittest.TestCase):
 def setUp(self):i18n.set_language('it')
 def tearDown(self):i18n.set_language('it')
 def app(self,keys=()):return app.App(FakeUI(keys))
 def test_only_requested_password_entries(self):
  self.assertEqual(app.passwords.FORMATS,('Custom','Diceware classico','Diceware BIP39'))
 def test_menu_header_up_then_centre(self):
  a=self.app(['UP','OK'])
  with self.assertRaises(app.Cancel):a.menu('Menu',['Uno','Due'])
  self.assertFalse(a.ui.back_focused)
 def test_menu_header_left_then_down(self):
  a=self.app(['LEFT','DOWN','DOWN','OK'])
  self.assertEqual(a.menu('Menu',['Uno','Due']),1)
 def test_note_back_without_k3(self):
  a=self.app(['UP','OK'])
  with self.assertRaises(app.Cancel):a.note('Avviso',['Test pubblico'])
  self.assertFalse(a.ui.back_focused)
 def test_words_back_without_k3(self):
  a=self.app(['UP','OK'])
  with self.assertRaises(app.Cancel):a.display_words(['abandon'],'Words')
  self.assertFalse(a.ui.back_focused)
 def test_secret_text_back_without_k3(self):
  a=self.app(['UP','OK'])
  with self.assertRaises(app.Cancel):a.text_result('PUBLIC-TEST')
  self.assertFalse(a.ui.back_focused)
 def test_dice_back_does_not_record_a_roll(self):
  a=self.app(['UP','OK'])
  with self.assertRaises(app.Cancel):a.collect(50)
  self.assertFalse(a.ui.back_focused)
 def test_dice_return_from_header_then_enter(self):
  a=self.app(['UP','DOWN','OK','OK'])
  self.assertEqual(a.collect(1),[1])
 def test_diagnostics_back_without_k3(self):
  a=self.app(['UP','OK']);a.diagnostics()
  self.assertFalse(a.ui.back_focused)
 def test_home_power_is_reachable_without_k3(self):
  a=self.app(['UP','OK','DOWN','OK']);focus=[]
  a.ui.home=lambda index:focus.append(index)
  called=[];a.power_menu=lambda:called.append(True)
  self.assertEqual(a.home(),0)
  self.assertEqual(focus,[0,4,4,0]);self.assertEqual(called,[True])
 def test_power_requires_explicit_confirmation(self):
  a=self.app();a.menu=lambda *args:0
  a.ui.shutdown_logo=lambda:None
  with patch.object(app.subprocess,'run') as power:a.shutdown();power.assert_not_called()
  a.menu=lambda *args:1
  with patch.object(app.subprocess,'run',side_effect=RuntimeError('power intercepted')) as power:
   with self.assertRaises(RuntimeError):a.shutdown()
   power.assert_called_once_with(['/sbin/poweroff'],check=True)
 def test_restart_tile_requires_confirmation(self):
  for confirmation in (0,1):
   a=self.app(['OK']);a.ui.power_menu=lambda index:None
   a.menu=lambda *args:confirmation
   with patch.object(app.subprocess,'run',side_effect=RuntimeError('reboot intercepted')) as reboot:
    if confirmation:
     with self.assertRaises(RuntimeError):a.power_menu()
     reboot.assert_called_once_with(['/sbin/reboot'],check=True)
    else:
     a.power_menu();reboot.assert_not_called()
 def test_power_menu_selects_shutdown_and_can_go_back(self):
  for keys,expected in ((['RIGHT','OK'],[True]),(['UP','OK'],[])):
   a=self.app(keys);a.ui.power_menu=lambda index:None
   called=[];a.shutdown=lambda:called.append(True)
   a.power_menu();self.assertEqual(called,expected)
 def test_password_settings_return_to_previous_step(self):
  a=self.app();a.wl=['public'];calls=[];actions=iter([0,app.Cancel(),1,2,0])
  def menu(title,options):
   calls.append(title);action=next(actions)
   if isinstance(action,Exception):raise action
   return action
  a.menu=menu
  alphabet,dictionary,bits,separator=a.password_settings(2)
  self.assertEqual(calls,['Forza password','Separatore','Forza password','Separatore','Fonte entropia'])
  self.assertEqual(bits,128);self.assertEqual(separator,'Space')
 def test_classic_route_still_generates_original_word_lengths(self):
  a=self.app();a.menu=lambda *args:2;record=[]
  a.generate=lambda count,dw:record.append((count,dw));a.password_flow(1)
  self.assertEqual(record,[(8,True)])
 def test_language_menu_updates_session_and_native_names(self):
  a=self.app(['DOWN','DOWN','OK']+['OK']*12);a.language_menu()
  self.assertEqual(i18n.language(),'fr')
  self.assertTrue(any('Langue choisie' in title for title,_,_ in a.ui.frames))
 def test_all_languages_have_native_labels_and_accents(self):
  self.assertEqual([v for _,v in i18n.LANGUAGES],['Italiano','English','Français','Español'])
  expected={'en':'Tools','fr':'Outils','es':'Herramientas'}
  for code,label in expected.items():
   i18n.set_language(code);self.assertEqual(i18n.tr('Strumenti'),label)
   self.assertNotEqual(i18n.tr('Conserva il foglio al sicuro.'),'Conserva il foglio al sicuro.')
 def test_dynamic_translation_and_page_titles(self):
  i18n.set_language('en')
  self.assertEqual(i18n.tr('Lancio 12/50'),'Roll 12/50')
  self.assertEqual(i18n.tr('Nuova seed BIP39 1/2'),'New BIP39 seed 1/2')
  self.assertEqual(i18n.tr('24 parole'),'24 words')
 def test_translation_placeholders_are_preserved(self):
  import re
  for key,values in i18n.CATALOG.items():
   tokens=re.findall(r'%(?:\.\d+)?[dsf]',key)
   for value in values.values():self.assertEqual(re.findall(r'%(?:\.\d+)?[dsf]',value),tokens)
 def test_secrets_and_dictionary_candidates_are_not_translated(self):
  for language in ('en','fr','es'):
   i18n.set_language(language)
   a=self.app(['OK']*100);a.text_result('Verifica Space Continua')
   self.assertEqual(''.join(line for _,lines,_ in a.ui.frames for line in lines),'Verifica Space Continua')
   a=self.app(['OK']);a.display_words(['Verifica','Space'],'Words')
   self.assertEqual(a.ui.frames[0][1],['01  Verifica','02  Space'])
   a=self.app(['OK']);self.assertEqual(a.choose_word(['Verifica','Space'],1),'Verifica')
 def test_startup_opens_home_without_confirmation(self):
  a=self.app();a.ui.splash=lambda:None
  a.note=Mock()
  a.home=lambda:(_ for _ in ()).throw(KeyboardInterrupt())
  with patch.object(app,'check_core',return_value=([],[],[('public','PASS')])):
   with self.assertRaises(KeyboardInterrupt):a.run()
  self.assertTrue(a.ready)
  a.note.assert_not_called()
 def test_language_validation(self):
  with self.assertRaises(ValueError):i18n.set_language('xx')
  self.assertEqual(i18n.language(),'it')
if __name__=='__main__':unittest.main(verbosity=2)
