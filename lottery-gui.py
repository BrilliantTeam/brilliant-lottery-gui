import tkinter as tk
from tkinter import ttk, messagebox
import random
import requests
from PIL import Image, ImageTk
from io import BytesIO

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("輝煌伺服器抽獎程式")
        self.root.geometry("810x550")
        self.root.resizable(False, False)
        
        try:
            response = requests.get("https://www.brilliantw.net/img/%E9%97%9C%E6%96%BC%E9%A3%AF%E5%A8%98/%E5%85%B6%E4%BB%96%E9%9D%9C%E6%85%8B%E9%A3%AF%E5%A8%98%E8%A1%A8%E6%83%85%E7%AC%A6%E8%99%9F/26.png")
            icon_image = Image.open(BytesIO(response.content))
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"無法載入圖標：：{e}")
        
        main_frame = ttk.Frame(root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        input_frame = ttk.LabelFrame(left_frame, text="輸入區域", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(input_frame, text="參與者名單：").pack(anchor=tk.W, pady=(0, 5))
        self.participants_text = tk.Text(input_frame, height=15, width=40)
        self.participants_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        settings_frame = ttk.Frame(input_frame)
        settings_frame.pack(fill=tk.X, pady=10)
        
        prize_frame = ttk.Frame(settings_frame)
        prize_frame.pack(fill=tk.X, pady=5)
        ttk.Label(prize_frame, text="獎品總數：", width=10).pack(side=tk.LEFT)
        self.total_prizes = ttk.Entry(prize_frame)
        self.total_prizes.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        winners_frame = ttk.Frame(settings_frame)
        winners_frame.pack(fill=tk.X, pady=5)
        ttk.Label(winners_frame, text="中獎人數：", width=10).pack(side=tk.LEFT)
        self.winners_count = ttk.Entry(winners_frame)
        self.winners_count.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="開始抽獎", command=self.draw, style='Accent.TButton'
                  ).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="清除所有", command=self.clear_all
                  ).pack(side=tk.LEFT, expand=True, padx=5)
        
        result_frame = ttk.LabelFrame(right_frame, text="抽獎結果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=15, width=40, state='disabled')
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        
        default_font = ('微軟正黑體', 11)
        self.participants_text.configure(font=default_font)
        self.result_text.configure(font=default_font)

    def draw(self):
        participants = self.participants_text.get("1.0", tk.END).strip().split('\n')
        participants = [p.strip() for p in participants if p.strip()]
        
        try:
            total_prizes = int(self.total_prizes.get())
            winners_count = int(self.winners_count.get())
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字！")
            return
            
        if not participants:
            messagebox.showerror("錯誤", "請輸入參與者名單！")
            return
        
        if total_prizes <= 0 or winners_count <= 0:
            messagebox.showerror("錯誤", "獎品總數和中獎人數必須大於 0！")
            return
            
        if winners_count > len(participants):
            messagebox.showerror("錯誤", "中獎人數不能大於參與者人數！")
            return
        
        winners = random.sample(participants, winners_count)
        
        prizes_per_person = total_prizes // winners_count
        remaining_prizes = total_prizes % winners_count
        
        self.result_text.config(state='normal')
        self.result_text.delete("1.0", tk.END)
        
        result_text = "　　　　　　　　🎉 抽獎結果 🎉\n"
        result_text += "─" * 30 + "\n\n"
        for i, winner in enumerate(winners, 1):
            prizes = prizes_per_person + (1 if i <= remaining_prizes else 0)
            result_text += f"┌─ {winner}\n"
            result_text += f"└─ 獲得 {prizes} 份獎品！\n\n"
        
        result_text += "─" * 30 + "\n"
        result_text += f"　　　　　　　　共 {len(winners)} 位中獎者\n"
        result_text += f"　　　　　　　　總計 {total_prizes} 份獎品"
        
        self.result_text.insert("1.0", result_text)
        self.result_text.config(state='disabled')

    def clear_all(self):
        self.participants_text.delete("1.0", tk.END)
        self.total_prizes.delete(0, tk.END)
        self.winners_count.delete(0, tk.END)
        self.result_text.config(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()