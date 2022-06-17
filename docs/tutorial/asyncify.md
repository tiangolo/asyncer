# Asyncify - Call Sync Code from Async Code

In many cases for **many projects** you will need to combine async code with blocking (non async) code.

If you run a function that just **blocks** and makes Python **wait** there without using `await`, it will prevent Python from jumping back and forth between all these concurrent async functions, because it will be just **waiting** there.

This is called to **block the event loop** (the event loop is the thing that runs the async functions in turns jumping at the `await` points).

Let's see how **Asyncer**'s `asyncify()` can help you with this.

## Block the Event Loop

Let's see a **broken** example first.

### Sync Work

Let's see a sync (regular, blocking) function `do_sync_work()`:

```Python hl_lines="3-5"
# Code above omitted 👆

{!./docs_src/tutorial/asyncify/tutorial001.py[ln:6-8]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
# 🚨 Don't use this, it will block the event loop! 🚨

{!./docs_src/tutorial/asyncify/tutorial001.py!}
```

</details>

This function could be talking to a database, a remote API, etc. But it doesn't use `await`, it just makes Python wait there without a warning using `time.sleep(1)`.

### Call Sync Code from Async Code Blocking

Here's the problem.

Let's just call that **slow** sync (regular, blocking) function directly from inside the async code 😱:

```Python hl_lines="14"
# 🚨 Don't use this, it will block the event loop! 🚨

{!./docs_src/tutorial/asyncify/tutorial001.py!}
```

Because that function is not async, but still it makes Python wait there, it will impede any other async code that could have been started from running. It will all have to **just wait** there doing nothing, wasting computation time. 😭

## Use Asyncify

In those cases where you want to run "**sync**" (synchronous, blocking) code **from inside of async** code in a way that is compatible with the rest of the async code you can use **Asyncer**'s `asyncify()`. 🚀

```Python hl_lines="4  13"
{!./docs_src/tutorial/asyncify/tutorial002.py!}
```

`asyncify()` takes the **sync (blocking) function** that you want to call and then returns another **async function** that takes the actual **arguments for the original sync function**.

Once you call that, **Asyncer** (using AnyIO) will run that function in a way that doesn't block the event loop.

Then you can `await` that and get the return value that was **safely** executed in a "**worker thread**" without blocking the event loop. 🎉

Notice that now the function `do_sync_work` is not an `async` function:

```Python hl_lines="3-5"
# Code above omitted 👆

{!./docs_src/tutorial/asyncify/tutorial002.py[ln:7-9]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/asyncify/tutorial002.py!}
```

</details>

...it even has a line:

```python
time.sleep(1)
```

...to simulate a blocking operation (that doesn't use `await`).

It could be reading a file, talking to a database, etc.

But `asyncify()` will do the right thing and run it on a *worker thread*. This way you can mix async code with blocking code more easily.

## Typing Support

And of course, because the way **Asyncer** is designed, you will get **typing support** with inline errors and autocompletion for the function arguments:

<img class="shadow" src="/docs/img/tutorial/asyncify/image01.png">

And you will also get **typing support** for the return value:

<img class="shadow" src="/docs/img/tutorial/asyncify/image02.png">

And if you used tools like **mypy** those would also be able to use this typing support to help you ensure your **code is correct** and prevent many bugs. 😎
