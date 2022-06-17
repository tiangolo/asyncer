# Syncify - Call Async Code from Sync Code

The same way you will probably need to use `asyncify()` to call **sync code** from **async code**, you will probably also need to call **async code** from **sync code**.

In those cases you can use `syncify()`. 🤓

* `asyncify()`: Call **sync code** from **async code**
* `syncify()`: Call **async code** from **sync code**

## Run Async Code from Blocking Code

Let's say that the **sync** (blocking) function that you run using `asyncify()` (that is run in a *worker thread* underneath) in turn, also needs to **call async code**.

But async functions can only be awaited inside of other async functions, you can't use `await` in the blocking function.

For these cases, where you are in **sync code** and need to **call an async function** from within the sync code in a way that is **sync-compatible**, you can use **Asyncer**'s `syncify()`:

```Python hl_lines="4  14"
{!./docs_src/tutorial/syncify/tutorial001.py!}
```

The way this will work, step by step, is like this:

* `anyio.run()` will start the async `main()` function.
* That **async** `main()` function will use `asyncify()` to call the regular, **sync** function `do_sync_work()` in a way compatible with async code (using `await`).
    * `asyncify()` will run the function on a **worker thread**.
* Then that regular/**sync** function `do_sync_work()` will call the **async** function `do_async_work()` using `syncify()`, in a way compatible with sync code (without using `await`).
    * `syncify()`, that was started from a **worker thread**, will send that **async** function to be run in the main thread running all the async code. Then it will take the result back to the worker thread and make it available, to put it in the variable `message`.

## Typing Support

Of course, as with the rest of **Asyncer**, you will get **typing support** for the function arguments, the return value, etc:

<img class="shadow" src="/docs/img/tutorial/syncify/image01.png">
