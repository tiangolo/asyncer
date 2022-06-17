# Runnify - Async Code With Arguments

Continuing with the last example, let's see the first use case where **Asyncer** could be useful. 🤓

## Async Main Function with Arguments

Let's say that now you want your async `main()` function to take arguments:

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/runnify/tutorial001.py[ln:10-12]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/runnify/tutorial001.py!}
```

</details>

## Runnify with Arguments

Now you can use `asyncer.runnify()` to run this function passing arguments:

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/runnify/tutorial001.py[ln:15]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/runnify/tutorial001.py!}
```

</details>

`asyncer.runnify()` takes the **async function** you want to call, and then it returns another function that **takes the positional and keyword arguments** needed, in this case it's just `name="World"`.

When you call that function with the arguments, it actually uses `anyio.run()` underneath to run the async function with the arguments.

And here's the advantage of this approach, you get **better typing support**.

For example, you will get editor **autocompletion**:

<img class="shadow" src="/docs/img/tutorial/runnify/image01.png">

And you will get editor **inline errors**:

<img class="shadow" src="/docs/img/tutorial/runnify/image02.png">

You will also get **mypy** support if you use it.

## Run the Program in the Command Line

If you run that, you will see the expected result, almost the same as with AnyIO, it will **wait for 1 second** and then print `Hello, World`:

<div class="termy">

```console
$ python main.py

// Wait for it...

// After around one second
Hello, World
```

</div>

## Next Steps

I'll show you next how to mix async code and regular (sync, blocking) code. 😎
