# Soonify - Return Values

In the last chapter, I showed you how to use `asyncer.soonify()` to run multiple async functions concurrently.

We wrote some code to call some **async functions** with some **arguments** *soon*, concurrently.

But what happens if you want to **retrieve the return value** from those async functions after they are run?

I'll show you how to do that here. 🤓

## Function Not Returning

Let's see the last example `do_work()` async function we used in the previous chapter:

```Python hl_lines="3-5"
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

This function takes a parameter `name` and then it prints a message.

But it **never returns** anything (which is equivalent to returning `None`).

## Return a Value

But now let's say that we don't really want that function to print the message directly, just to **return** the string.

Maybe because we could want to do something else later with the value, or for any other reason:

```Python hl_lines="5-6"
# Code above omitted 👆

{!./docs_src/tutorial/soonify_return/tutorial001.py[ln:5-8]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify_return/tutorial001.py!}
```

</details>

## Store `SoonValue` Objects

When you use:

```python
task_group.soonify(async_function)(arg1, arg2)
```

...that call **returns a special object** (an instance of a class `SoonValue`) that you can store in a variable:

```Python hl_lines="11-13"
# Code above omitted 👆

{!./docs_src/tutorial/soonify_return/tutorial001.py[ln:5-15]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify_return/tutorial001.py!}
```

</details>

## Get the Return Value from `SoonValue` Objects

When one of these async functions started with `soonify()` finishes, the **return value** of the function is **stored** inside the `SoonValue` object, in the **attribute** `soon_value1.value`:

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/soonify_return/tutorial001.py[ln:11-18]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify_return/tutorial001.py!}
```

</details>

After the `async with` block, the **task group** will wait for all of the concurrent functions/tasks to finish **before** any code below is executed.

This means that after the `async with` block those functions will have already **finished**, and the `SoonValue` objects will **contain** the **return value** already.

## Typing Support

Because of the way **Asyncer** is designed, you will get **typing support** in these `SoonValue` objects and their `soon_value1.value` attribute.

This means that your editor will know the type of that `soon_value1.value`, and will be able to provide you **autocompletion**:

<img class="shadow" src="/docs/img/tutorial/soonify-return/image01.png">

And because the editor knows the types of the values, you will also get **inline errors**:

<img class="shadow" src="/docs/img/tutorial/soonify-return/image02.png">

And because the editor can follow and **infer** this type information, you will also get **type support** down the line in anything that uses these values.

For example, it will be able to infer that `get_data()` returns a list of strings.

And when you `await` and access the return value of `get_data()` you will also get editor support:

<img class="shadow" src="/docs/img/tutorial/soonify-return/image03.png">

Notice that you didn't even have to add the type to most of the variables, only to the function parameters, and everything else was **inferred**.

All this **typing support** also means that you can use tools like **mypy** to verify that your code is **correct** and prevent many bugs.

## `SoonValue` Objects Inside the `async with` Block

If you try to access the `soon_value1.value` attribute of the `SoonValue` object **inside** the `async with` block, you will **normally get an error**:

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/soonify_return/tutorial002.py[ln:11-19]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify_return/tutorial002.py!}
```

</details>

That will raise an exception like this:

> `PendingValueException`: The return value of this task is still pending.
Maybe you forgot to access it after the `async with asyncer.create_task_group()` block. If you need to access values of async tasks inside the same task group, you probably need a different approach, for example with AnyIO Streams.

That `print(soon_value1.value)` is still inside the `async with` block for the **task group**. And by that point, **none** of those async functions have been **run yet**.

Remember that the end of the `async with` block acts as if it had **an implicit `await`**.

At the end of the `async with` block, Python will **run any async code that is pending** (in this case, the async functions you passed to `soonify()`). It will wait for that to finish before continuing below.

And when Python continues below that `async with` block, as **all the async functions** were **already called and awaited**, all the `SoonValue` objects will **have** their `soon_value1.value` attributes **available**.

But before the values are available, trying to access them will raise that exception.

## Check When a `SoonValue` Object is `ready`

If there are some `await` points inside of the `async with` block, Python would go and **run pending async code** at those `await` points (including the async functions you passed to `soonify()`).

Because of that, the `soon_value1.value` attributes of the `SoonValue` objects **could have their value available**, even inside of the `async with` block.

You can check if the value is already available by using the `soon_value.ready` attribute, it will be `True` or `False`:

```Python hl_lines="6-8" linenums="1"
# Code above omitted 👆

{!./docs_src/tutorial/soonify_return/tutorial003.py[ln:11-16]!}

        # Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/soonify_return/tutorial003.py!}
```

</details>

Here we have an `await` inside the `async with` block. It sleeps for **2 seconds**.

Because it's an `await`, it will tell Python to go and **run** any other **pending async code**.

So, Python will run (or at least start) the pending async function we passed to `soonify()`.

The **2 seconds** is more than what the function will take to finish because it waited for **1 second** inside. So, after that `await`, the `soon_value1.value` attribute will be available.

We verify that first, checking that `soon_value1.ready` is `True`, and then we can safely print the value.

!!! tip
    If you feel like you need to **access** values **generated** by the async functions **inside** the same `async with` block for a **task group**, you might need to use a different approach, for example, with <a href="https://anyio.readthedocs.io/en/stable/streams.html" class="external-link" target="_blank">AnyIO Streams</a>.
