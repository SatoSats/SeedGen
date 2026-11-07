"""Host tests: no GPIO, no display, public fixtures only."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('v5',Path(__file__).with_name('main.py'))
v5=importlib.util.module_from_spec(spec); spec.loader.exec_module(v5)

class FakeUI:
    def __init__(self,keys=()): self.keys=iter(keys); self.frames=[]
    def key(self): return next(self.keys)
    def render(self,title,lines=(),footer=''): self.frames.append((title,list(lines),footer))

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.wl,cls.dw,cls.results=v5.check_core()
    def app(self,keys=()):
        a=v5.App(FakeUI(keys)); a.wl=self.wl; a.dw=self.dw; return a
    def test_original_tests(self):
        self.assertEqual(len(self.results),14)
        self.assertTrue(all(s=='PASS' for _,s in self.results))
    def test_all_lengths_and_checksum(self):
        for n in v5.LENGTHS:
            ent=bytes(v5.core.ENTROPY_BITS[n]//8)
            words=v5.core.entropy_to_mnemonic(ent,self.wl)
            self.assertEqual(len(words),n)
            self.assertEqual(v5.core.mnemonic_to_entropy(words,self.wl),ent)
        with self.assertRaises(ValueError): v5.core.mnemonic_to_entropy(['abandon']*12,self.wl)
    def test_diceware_all_indices(self):
        for index in range(7776):
            rolls=v5.core.encode_base6(index,5)
            self.assertEqual(v5.diceware_words(rolls,self.dw),[self.dw[index]])
    def test_invalid_dice(self):
        for rolls in ([],[1]*4,[0]*5,[7]*5,['1']*5):
            with self.assertRaises(ValueError): v5.diceware_words(rolls,self.dw)
    def test_audit_parameters(self):
        for n,expected in zip(v5.LENGTHS,(50,62,75,87,100)):
            bits,N,k,p=v5.audit_parameters(n)
            self.assertEqual(N,expected); self.assertGreaterEqual(k,bits)
            self.assertEqual(p,v5.core.acceptance_probability(bits))
    def test_menu_scroll_and_wrap(self):
        a=self.app(['DOWN']*10+['OK'])
        self.assertEqual(a.menu('Menu',v5.MAIN_MENU),10)
        self.assertIn('> Spegni Raspberry',a.ui.frames[-1][1])
        a=self.app(['UP','DOWN','OK']); self.assertEqual(a.menu('Menu',v5.MAIN_MENU),0)
    def test_large_font_word_pages(self):
        words=self.wl[:12]
        a=self.app(['OK','OK','OK'])
        a.display_words(words,'Seed BIP39')
        shown=[line.strip()[4:] for _,lines,_ in a.ui.frames for line in lines]
        self.assertEqual(shown,words)
        self.assertTrue(all(len(lines)<=5 for _,lines,_ in a.ui.frames))
        font=v5.body_font()
        for word in self.wl+self.dw:
            self.assertLessEqual(font.getlength('24  '+word),224)

    def test_note_pages_preserve_text(self):
        lines=['Un messaggio lungo da leggere completamente sul piccolo display.']*4
        wrapped=v5.wrap_lines(lines,v5.body_font())
        a=self.app(['OK']*20)
        a.note('Avviso',lines)
        shown=[line for _,items,_ in a.ui.frames for line in items]
        self.assertEqual(shown,wrapped)
        self.assertTrue(all(len(items)<=5 for _,items,_ in a.ui.frames))

    def test_menu_cancel(self):
        with self.assertRaises(v5.Cancel): self.app(['BACK']).menu('Menu',v5.MAIN_MENU)
    def test_correct_final_roll(self):
        a=self.app(['OK','OK','DOWN','OK','RIGHT','OK','OK'])
        self.assertEqual(a.collect(2),[1,2])
    def test_undo_and_cancel(self):
        with self.assertRaises(v5.Cancel): self.app(['OK','K1','BACK']).collect(2)
    def test_choose_prefix(self):
        a=self.app(['OK','OK','OK']); self.assertEqual(a.choose_word(['aa','ab','ac','ad','ae','af','ag','ah'],1),'aa')
    def test_full_copy_and_mismatch(self):
        a=self.app(); a.note=lambda *args:None
        entered=iter(['ability','abandon'])
        a.choose_word=lambda *args:next(entered); a.menu=lambda *args:0
        a.verify_copy(['abandon'],self.wl)
        entered=iter(['ability']); a.choose_word=lambda *args:next(entered); a.menu=lambda *args:2
        with self.assertRaises(v5.Cancel): a.verify_copy(['abandon'],self.wl)
    def test_copy_bip39_validates_reentered_words_before_confirmation(self):
        words = v5.core.entropy_to_mnemonic(bytes(16), self.wl)
        entered = iter(words)
        a = self.app()
        a.choose_word = lambda *args: next(entered)
        with patch.object(v5.core, 'mnemonic_to_entropy', wraps=v5.core.mnemonic_to_entropy) as check:
            def note(title, lines):
                if title == 'Copia verificata':
                    check.assert_called_once_with(words, self.wl)
            a.note = note
            a.verify_copy(words, self.wl, bip39=True)
            check.assert_called_once_with(words, self.wl)

    def test_identical_copy_with_invalid_bip39_checksum_cannot_be_verified(self):
        words = ['abandon'] * 12
        entered = iter(words)
        a = self.app()
        notes = []
        a.note = lambda title, lines: notes.append(title)
        a.choose_word = lambda *args: next(entered)
        def cancel(title, options):
            self.assertEqual(title, 'Copia non verificata')
            self.assertEqual(options, ['Riprova dal foglio', 'Annulla (non verificata)'])
            return 1
        a.menu = cancel
        with self.assertRaises(v5.Cancel):
            a.verify_copy(words, self.wl, bip39=True)
        self.assertNotIn('Copia verificata', notes)

    def test_copy_bip39_can_retry_after_unexpected_validation_error(self):
        entropy = bytes(16)
        words = v5.core.entropy_to_mnemonic(entropy, self.wl)
        entered = iter(words * 2)
        a = self.app()
        notes = []
        a.note = lambda title, lines: notes.append(title)
        a.choose_word = lambda *args: next(entered)
        def retry(title, options):
            self.assertEqual(title, 'Copia non verificata')
            self.assertNotIn('Copia verificata', notes)
            return 0
        a.menu = retry
        with patch.object(v5.core, 'mnemonic_to_entropy', side_effect=[RuntimeError('public test failure'), entropy]) as check:
            a.verify_copy(words, self.wl, bip39=True)
        self.assertEqual(check.call_count, 2)
        self.assertEqual(notes.count('Copia verificata'), 1)

    def test_mnemonic_valid_invalid(self):
        for valid in (True,False):
            a=self.app(); a.menu=lambda *args:0; notes=[]
            a.note=lambda title,*args:notes.append(title)
            words=iter(v5.core.entropy_to_mnemonic(bytes(16),self.wl) if valid else ['abandon']*12)
            a.choose_word=lambda *args:next(words)
            with patch.object(v5,'require_offline'): a.verify_mnemonic()
            self.assertIn('Checksum BIP39 valido' if valid else 'Mnemonic non valida',notes)
    def test_generation_both_flows(self):
        for count,dw in [(n,False) for n in v5.LENGTHS]+[(n,True) for n in (6,7,8,9)]:
            a=self.app(); a.note=lambda *args:None
            # Fixed balanced public fixture known accepted by the original extractor.
            N=count*5 if dw else v5.core.dice_rolls_needed(v5.core.ENTROPY_BITS[count])
            rolls=([1,2,3,4,5,6]*20)[:N]
            if not dw:
                while not v5.core.extract_entropy_from_dice_block(rolls,v5.core.ENTROPY_BITS[count])[2]:
                    rolls=v5.core.encode_base6(0,N)  # fallback covered only as deterministic core fixture
            a.collect=lambda n:list(rolls)
            shown=[]; verified=[]
            a.display_words=lambda words,title:shown.extend(words)
            def verify(words, dictionary, *, bip39):
                self.assertEqual(bip39, not dw)
                verified.extend(words)
            a.verify_copy = verify
            with patch.object(v5,'require_offline'),patch.object(v5.core,'analizza_distribuzione_lanci',return_value=(True,20)):
                a.generate(count,dw)
            self.assertEqual(len(shown),count); self.assertEqual(shown,verified)
    def test_rejection_and_distribution_redo(self):
        a=self.app(); notes=[]; a.note=lambda title,*args:notes.append(title)
        N=v5.core.dice_rolls_needed(128)
        public=([1,2,3,4,5,6]*10)[:N]
        rejected = ([6,5,4,3,2,1]*10)[:N]
        self.assertTrue(v5.core.analizza_distribuzione_lanci(rejected)[0])
        self.assertFalse(v5.core.extract_entropy_from_dice_block(rejected, 128)[2])
        blocks = iter([rejected, [1]*N, public])
        a.collect = lambda n: next(blocks)
        a.display_words = lambda *args: None
        a.verify_copy = lambda *args, **kwargs: None
        with patch.object(v5, 'require_offline'):
            a.generate(12)
        self.assertIn('Blocco rifiutato',notes)
        self.assertIn('Distribuzione anomala',notes)

    def test_guard_blocks_network_and_swap(self):
        a=self.app()
        with patch.object(v5,'require_offline',side_effect=RuntimeError('offline')):
            with self.assertRaises(RuntimeError): a.generate(12)
    def test_guard_reads_network_and_swap_state(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            root = Path(directory)
            network = root / 'net'
            interface = network / 'eth0'
            interface.mkdir(parents=True)
            flags = interface / 'flags'
            swaps = root / 'swaps'
            swaps.write_text('Filename Type Size Used Priority\n')
            flags.write_text('0x0\n')
            paths = {'/proc/swaps': swaps, '/sys/class/net': network}
            with patch.object(v5, 'Path', side_effect=paths.__getitem__):
                v5.require_offline()
                flags.write_text('0x1\n')
                with self.assertRaisesRegex(RuntimeError, 'rete'):
                    v5.require_offline()
                flags.write_text('0x0\n')
                swaps.write_text('Filename Type Size Used Priority\n/test file 1 0 -2\n')
                with self.assertRaisesRegex(RuntimeError, 'Swap'):
                    v5.require_offline()

    def test_startup_self_test_fail_blocks_generation(self):
        a = self.app()
        with patch.object(a.ui, 'splash', create=True), \
             patch.object(v5.core, 'run_all_self_tests', return_value=[('fixture', 'FAIL')]), \
             patch.object(a, 'home') as home:
            with self.assertRaisesRegex(RuntimeError, 'Self-test'):
                a.run()
        self.assertFalse(a.ready)
        home.assert_not_called()

    def test_cancelled_dice_generation_displays_no_mnemonic(self):
        a = self.app()
        a.note = lambda *args: None
        with patch.object(v5, 'require_offline'), \
             patch.object(a, 'collect', side_effect=v5.Cancel), \
             patch.object(a, 'display_words') as display, \
             patch.object(a, 'verify_copy') as verify:
            with self.assertRaises(v5.Cancel):
                a.generate(12)
        display.assert_not_called()
        verify.assert_not_called()
        self.assertEqual(a.ui.frames[-1][0], 'Sessione chiusa')

    def test_hash_tamper_fails(self):
        with patch.object(v5,'CORE_SHA256','0'*64):
            with self.assertRaises(RuntimeError): v5.check_core()

if __name__=='__main__': unittest.main(verbosity=2)
