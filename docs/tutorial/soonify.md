# Soonify - Concurrent Code

The main point of async code is to be able to run things **concurrently**. That means running multiple async functions **during the same period of time**.

That way, while Python waits (in one of the `await` parts) for something to finish, it can work in another of the async functions.

## Async Code - Not Concurrent

Let's start by just calling an **async function 3 times**, one after the other.

This is still **not concurrent** because Python will run each one in its turn:

```Python hl_lines="3-9"
# Code above omitted 👆

{!./docs_src/tutorial/soonify/tutorial001.py[ln:9-12]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
# 🚨 This is not concurrent 🚨

{!./docs_src/tutorial/soonify/tutorial001.py!}
```

</details>

Python will see the first `await`, then it will know that **this might take a while**.

Now Python could run something else that was **already waiting** somewhere else.

But we didn't tell Python to run anything else **during this same period of time**.

So Python will just come back and **wait** for the first `await` to finish.

Then Python will see the next line to execute and will do all that again.

So, although we use `async` and `await` here, this code is not concurrent, at least not the calls to `do_work()`.

If you have **something else** running it (for example, a **FastAPI** app), then it will let Python go and do other things during those `await`s (for example, handle other requests). That way the program would take **some advantage** of `async` and `await`.

But the calls to `do_work()` are **not concurrent** inside of `get_data()`.

## Async Code - Concurrent

Let's now use **Asyncer** to run these **3 functions concurrently**. 🎉

### Task Group

Use **Asyncer**'s `create_task_group()` in an `async with` block to create a **task group** object:

```Python hl_lines="3  8"
# Code above omitted 👆

{!./docs_src/tutorial/soonify/tutorial002.py[ln:2]!}

# Code here omitted 👈

{!./docs_src/tutorial/soonify/tutorial002.py[ln:10-11]!}
        # Code here omitted 👈

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify/tutorial002.py!}
```

</details>

## Task Group - Soonify One Function

Now use `task_group.soonify()` to tell it to run the first function *soon* (that's why it's called "`soonify()`").

Pass it the async function to call.

That returns another function that receives the **arguments** for the async function you want to call:

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/soonify/tutorial002.py[ln:2]!}

# Code here omitted 👈

{!./docs_src/tutorial/soonify/tutorial002.py[ln:10-12]!}
        # Code here omitted 👈

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify/tutorial002.py!}
```

</details>

This tells this **task group** to run that function **soon**.

It **won't run it right away** and make Python wait for it. Instead, the **task group** will first receive all the things you want to run and then call them *concurrently*: **during the same period of time**.

## Task Group - Soonify More Functions

Now you can use the same `task_group.soonify()` to **add the other async functions** you want to call concurrently with their parameters:

```Python hl_lines="9-11"
# Code above omitted 👆

{!./docs_src/tutorial/soonify/tutorial002.py[ln:2]!}

# Code here omitted 👈

{!./docs_src/tutorial/soonify/tutorial002.py[ln:10-14]!}
    # Code here omitted 👈

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify/tutorial002.py!}
```

</details>

After the `async with` block ends, Python takes it as if it had an implicit `await` there.

At that point, this **task group** will run those async functions **concurrently**.

Python will wait for all that to end in that `async with` block. It's like if the `async with` block had an implicit `await` at the end.

## Review All the Code

```Python
{!./docs_src/tutorial/soonify/tutorial002.py!}
```

Python will start with the first async function call to `do_work()` with the parameters `name="Yury"`.

It will start that `anyio.sleep(1)` and it will notice the `await` there:

```Python hl_lines="4"
# Code above omitted 👆

{!./docs_src/tutorial/soonify/tutorial002.py[ln:5-7]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify/tutorial002.py!}
```

</details>


That's the cue for Python to go and **run anything else** that might be **pending**.

At that point, Python will notice another thing **pending to run**, the next call to `do_work()` with the arguments `name="Nathaniel"`. It will run it, notice the `await`, etc.

At some point it will get back to the first `await` and see that it's now done, so it will continue with that code, and print a message:

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/soonify/tutorial002.py[ln:5-7]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify/tutorial002.py!}
```

</details>

Because this was the first call, with `name="Yury"`, it will print:

```
Hello, Yury
```

After that, this function call to `do_work()` is done. There's nothing else to run in it.

Then Python will continue with the **next thing pending**. And that will be another `await` for `do_work()` with the arguments `name="Nathaniel"`.

So now it will print:

```
Hello, Nathaniel
```

At some point, Python will end running all the things from this **task group**.

That will be the end of the `async with` block for the task group, and Python will continue executing whatever is next.

## Run the Program in the Command Line

If you run the program in the **command line**, you will see that it will be silent for around **1 second**.

And then it will print about **everything at once**.

This is because Python was **waiting** for all those `anyio.sleep(1)` calls **concurrently**.

So, Python was **waiting 1 second** in **3 places**. But in each of those, it **started waiting at around the same time**, so it will only **take around 1 second** for it to run, **instead of 3 seconds**:

<div class="termy">

```console
$ python main.py

// Enjoy the silence...


// All the output at once! 🎉
Hello, Yury
Hello, Nathaniel
Hello, Alex
```

</div>

## Type Support

Now, because of the way **Asyncer** is designed, you will get typing support for your code.

This means that you will have **autocompletion** in your editor for the original arguments of the async function to call:

<img class="shadow" src="/docs/img/tutorial/soonify/image01.png">

And you will have inline errors in your editor too:

<img class="shadow" src="/docs/img/tutorial/soonify/image02.png">

If you use tools like **mypy**, those tools will also be able to help you detect those possible errors.

This can help you write code more **efficiently** and with more **confidence** that it's **correct**. And it will also make sure that whenever you **refactor** it, you are not **breaking** anything somewhere else. 😎

## Next Steps

Next I'll show you how to run async functions concurrently and **retrieve their return values**. 🚀
