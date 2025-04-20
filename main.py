# main.py — Kivy-based RoyalWin AI Android Coach

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from ai_coach_app import AICoach

class AICoachUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.coach = AICoach()
        self.history = []

        Window.clearcolor = (0.08, 0.08, 0.1, 1)

        self.balance_label = Label(text="💼 Balance: ₹0", font_size=16, size_hint_y=None, height=30)
        self.add_widget(self.balance_label)

        self.balance_input = TextInput(hint_text="Enter starting balance", multiline=False)
        self.add_widget(self.balance_input)

        self.set_balance_btn = Button(text="Set Balance", on_press=self.set_balance)
        self.add_widget(self.set_balance_btn)

        self.history_input = TextInput(hint_text="Enter past results (e.g. 9,10,12)", multiline=False)
        self.add_widget(self.history_input)

        self.add_history_btn = Button(text="Add History", on_press=self.load_history)
        self.add_widget(self.add_history_btn)

        self.predict_btn = Button(text="🔮 Predict Next", on_press=self.predict)
        self.add_widget(self.predict_btn)

        self.result_input = TextInput(hint_text="Enter latest result (3–18)", multiline=False)
        self.add_widget(self.result_input)

        self.submit_result_btn = Button(text="✅ Submit Result", on_press=self.submit_result)
        self.add_widget(self.submit_result_btn)

        self.output = Label(text="Welcome to Quantum AI Coach!", size_hint_y=None, height=400)
        scroll = ScrollView()
        scroll.add_widget(self.output)
        self.add_widget(scroll)

    def popup(self, msg):
        popup = Popup(title='Alert', content=Label(text=msg), size_hint=(0.8, 0.4))
        popup.open()

    def set_balance(self, instance):
        try:
            amt = int(self.balance_input.text)
            self.coach.balance = amt
            self.balance_label.text = f"💼 Balance: ₹{amt}"
        except:
            self.popup("Please enter a valid number.")

    def load_history(self, instance):
        try:
            nums = [int(x.strip()) for x in self.history_input.text.split(',') if 3 <= int(x.strip()) <= 18]
            for num in nums:
                self.history.append(num)
                self.coach.learn(num)
            self.output.text += f"\n📥 History Added: {nums}"
        except:
            self.popup("Invalid input. Use format: 9,10,11")

    def predict(self, instance):
        pred, conf, number, reason = self.coach.predict_next()
        stake = self.coach.next_stake()
        next_stake = self.coach.next_after_loss()
        self.output.text += f"\n\n🔮 Prediction: {pred.upper()} | Number: {number} | Confidence: {conf}%\n💸 Stake: ₹{stake} ➝ Next: ₹{next_stake}\n📊 {reason}"

    def submit_result(self, instance):
        try:
            val = int(self.result_input.text.strip())
            self.history.append(val)
            win, stake, _ = self.coach.evaluate_result(val)
            summary = self.coach.get_summary()
            result = "✅ WIN" if win else "❌ LOSS"
            self.output.text += f"\n\n🎯 Result: {val} ➝ {result}\n🏆 W: {summary['wins']} | L: {summary['losses']} | ₹{summary['profit']} | Acc: {summary['accuracy']}%"
            self.balance_label.text = f"💼 Balance: ₹{summary['balance']}"
        except:
            self.popup("Please enter a valid number between 3–18.")

class RoyalWinApp(App):
    def build(self):
        return AICoachUI()

if __name__ == '__main__':
    RoyalWinApp().run()
