![benten and neko](https://github.com/sotw/benten_memo/blob/main/001small.png?raw=true)

# Benten Memo

An personal Console Memo focus on Taiwan stock.

# How to use

The basic flow is 

1. Add note 
   
   ```
   benten_memo -a [stock number]:[note]
   ```

2. Update basic information and list note
   
   ```
   benten_memo -u
   ```
   
   you can add number to list all spicific target stock's memo
   
   ```
   benten_memo -u [stock number]
   ```

3. To read memo without update current information
   
   ```
   benten_memo -s
   ```

4. Delete Note
   
   ```
   benten_memo -k [note id]
   ```

There are also global memo for some insight sparks on your head.

1. Add global note
   
   ```
   benten_memo -ag [note]
   ```

2. Read global note
   
   ```
   benten_memo -sg
   ```

3. Delete global note
   
   ```
   benten_memo -kg [memo number]
   ```

4. Delete specific note
   
   ```
   benten_memo -k [number]
   ```

# What's new

[FEATURE] COROUTIE implemented when issue benten_memo -u

# To do

[FEATURE] import data from simple txt file
[FEATURE] export data from database
