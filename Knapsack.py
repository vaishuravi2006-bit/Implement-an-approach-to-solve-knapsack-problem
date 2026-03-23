import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# -----------------------------
# Item Class
# -----------------------------

class Item:
    def __init__(self,name,weight,value):
        self.name=name
        self.weight=weight
        self.value=value

    def ratio(self):
        if self.weight==0:
            return 0
        return self.value/self.weight


# -----------------------------
# Global Storage
# -----------------------------

items=[]
capacity=30


# -----------------------------
# Load CSV
# -----------------------------

def load_csv():

    global items

    file=filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])

    if not file:
        return

    try:
        df=pd.read_csv(file)

        items=[]

        for _,row in df.iterrows():
            items.append(Item(str(row["name"]),int(row["weight"]),int(row["value"])))

        update_list()
        status.set("CSV loaded successfully")

    except Exception as e:
        messagebox.showerror("Error",str(e))


# -----------------------------
# Load Excel
# -----------------------------

def load_excel():

    global items

    file=filedialog.askopenfilename(filetypes=[("Excel files","*.xlsx")])

    if not file:
        return

    try:
        df=pd.read_excel(file)

        items=[]

        for _,row in df.iterrows():
            items.append(Item(str(row["name"]),int(row["weight"]),int(row["value"])))

        update_list()
        status.set("Excel loaded successfully")

    except Exception as e:
        messagebox.showerror("Error",str(e))


# -----------------------------
# Save CSV
# -----------------------------

def save_csv():

    if not items:
        messagebox.showinfo("Info","No items to save")
        return

    file=filedialog.asksaveasfilename(defaultextension=".csv")

    if not file:
        return

    data={"name":[i.name for i in items],
          "weight":[i.weight for i in items],
          "value":[i.value for i in items]}

    pd.DataFrame(data).to_csv(file,index=False)

    status.set("Data saved")


# -----------------------------
# Add Item
# -----------------------------

def add_item():

    try:
        name=name_entry.get()

        weight=int(weight_entry.get())
        value=int(value_entry.get())

        if name=="":
            raise ValueError("Name required")

        items.append(Item(name,weight,value))

        update_list()

        name_entry.delete(0,tk.END)
        weight_entry.delete(0,tk.END)
        value_entry.delete(0,tk.END)

    except:
        messagebox.showerror("Error","Invalid input")


# -----------------------------
# Update List Display
# -----------------------------

def update_list():

    listbox.delete(0,tk.END)

    for i,item in enumerate(items):

        listbox.insert(tk.END,
        f"{i+1}. {item.name} | W:{item.weight} V:{item.value} R:{round(item.ratio(),2)}")


# -----------------------------
# Greedy Algorithm
# -----------------------------

def greedy_knapsack():

    start=time.time()

    sorted_items=sorted(items,key=lambda x:x.ratio(),reverse=True)

    selected=[]
    total_weight=0
    total_value=0

    for item in sorted_items:

        if total_weight+item.weight<=capacity:

            selected.append(item)

            total_weight+=item.weight
            total_value+=item.value

    runtime=time.time()-start

    return selected,total_weight,total_value,runtime


# -----------------------------
# Dynamic Programming
# -----------------------------

def dp_knapsack():

    start=time.time()

    n=len(items)

    dp=[[0]*(capacity+1) for _ in range(n+1)]

    for i in range(1,n+1):

        wt=items[i-1].weight
        val=items[i-1].value

        for w in range(capacity+1):

            if wt<=w:

                dp[i][w]=max(val+dp[i-1][w-wt],dp[i-1][w])

            else:

                dp[i][w]=dp[i-1][w]

    w=capacity
    selected=[]

    for i in range(n,0,-1):

        if dp[i][w]!=dp[i-1][w]:

            item=items[i-1]

            selected.append(item)

            w-=item.weight

    total_weight=sum(i.weight for i in selected)
    total_value=sum(i.value for i in selected)

    runtime=time.time()-start

    return selected,total_weight,total_value,runtime


# -----------------------------
# Smart Optimizer
# -----------------------------

def optimize():

    if not items:
        messagebox.showinfo("Info","No items loaded")
        return

    if len(items)>40:

        result=greedy_knapsack()

        show_result("Greedy",result)

    else:

        g=greedy_knapsack()
        d=dp_knapsack()

        if d[2]>g[2]:
            show_result("Dynamic Programming",d)
        else:
            show_result("Greedy",g)


# -----------------------------
# Show Result
# -----------------------------

def show_result(name,data):

    selected,w,v,time_taken=data

    result_box.delete(0,tk.END)

    result_box.insert(tk.END,f"Algorithm: {name}")

    for item in selected:

        result_box.insert(tk.END,f"{item.name} (W:{item.weight},V:{item.value})")

    result_box.insert(tk.END,f"Total Weight: {w}")
    result_box.insert(tk.END,f"Total Value: {v}")
    result_box.insert(tk.END,f"Runtime: {round(time_taken,5)} sec")


# -----------------------------
# Smart Recommendation
# -----------------------------

def recommend():

    if not items:
        return

    result_box.delete(0,tk.END)

    result_box.insert(tk.END,"Recommended High Efficiency Items")

    for item in items:

        if item.ratio()>6:

            result_box.insert(tk.END,f"{item.name} (ratio {round(item.ratio(),2)})")


# -----------------------------
# Graph Visualization
# -----------------------------

def show_graph():

    if not items:
        return

    weights=[i.weight for i in items]
    values=[i.value for i in items]

    plt.scatter(weights,values)

    plt.xlabel("Weight")
    plt.ylabel("Value")
    plt.title("Warehouse Item Distribution")

    plt.show()


# -----------------------------
# GUI
# -----------------------------

root=tk.Tk()

root.title("Smart Warehouse Optimizer")
root.geometry("750x650")

title=tk.Label(root,text="Warehouse Shelf Optimization System",font=("Arial",16))
title.pack(pady=10)

frame=tk.Frame(root)
frame.pack()

tk.Label(frame,text="Name").grid(row=0,column=0)
tk.Label(frame,text="Weight").grid(row=0,column=1)
tk.Label(frame,text="Value").grid(row=0,column=2)

name_entry=tk.Entry(frame)
weight_entry=tk.Entry(frame)
value_entry=tk.Entry(frame)

name_entry.grid(row=1,column=0)
weight_entry.grid(row=1,column=1)
value_entry.grid(row=1,column=2)

tk.Button(frame,text="Add Item",command=add_item).grid(row=1,column=3,padx=10)

listbox=tk.Listbox(root,width=80,height=10)
listbox.pack(pady=10)

btn_frame=tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame,text="Load CSV",command=load_csv).grid(row=0,column=0,padx=5)
tk.Button(btn_frame,text="Load Excel",command=load_excel).grid(row=0,column=1,padx=5)
tk.Button(btn_frame,text="Save CSV",command=save_csv).grid(row=0,column=2,padx=5)
tk.Button(btn_frame,text="Optimize",command=optimize).grid(row=0,column=3,padx=5)
tk.Button(btn_frame,text="Recommendations",command=recommend).grid(row=0,column=4,padx=5)
tk.Button(btn_frame,text="Show Graph",command=show_graph).grid(row=0,column=5,padx=5)

result_box=tk.Listbox(root,width=80,height=10)
result_box.pack(pady=10)

status=tk.StringVar()
status.set("Ready")

status_bar=tk.Label(root,textvariable=status)
status_bar.pack()

root.mainloop()
