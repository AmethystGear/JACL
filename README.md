# JACL
Just Another Configuration Language

Basically what the title says, more or less.

For some reason, lots of people love using JSON as a configuration format. Which sucks. For a number of reasons, including:
1. No comments in JSON (Seriously, you'd think this would need to be the only one on the list.)
2. everything needs to be a hashmap (with string keys... ew)
3. no trailing commas (sucks when you're trying to hand roll it out)
4. Can I get an ordered hashmap? No? Ok, thanks.

and many more!

Yeah, you could use YAML or XML, but those have their own problems. JSON syntax feels like it's 80% of the way to a config format. So why not make something that borrows from JSON syntax, but fixes a lot of the problems?

Enter JACL. JACL is a superset of JSON that fixes most of JSON's problems (for configs)! Since it's a strict superset, you can plug your JSON right into JACL. We wont mind!

## Hello JACL
Let's start with the most basic config file possible:
```
0
```
In JACL, any primitive or collection sitting alone in a file is 100% ok. That means i can do:
```
"hello world"
```
or
```
1 2 3 4 5
```
but what if I want to name my data? Well, there are two ways you can go about this.
## I'm lazy and just want a Hashmap damn it/the JSON way
```
"I'm" : "lazy"
"and" : "just"
"want" : "a"
"Hashmap" : "damn"
.
.
```
## I like my objects to be objects thank you very much
```
zip_code : 78320
name : "John Doe"
```
Notice in the first case, your strings can be anything, but in the second, they have to be valid variable names. This is done so that we can have easy mappings from .jacl files to structs/objects.

So far, we've been dealing with pretty flat examples. But you can nest stuff any way you like. Behold:
```
[ "hello" "world!" ":)" ]
[ "bye bye" "world!" "See you tommorrow!" ]
[ "beep" "boop" ]
```
an array of arrays!
```
gamemodes : {
  "pvp" : (
    ...fields...
  )
  "pve" : (
    ...fields...
  )
}
```
hashmaps with objects inside of them!

etc.

we also have an extra collection, the Ordered Hashmap. This is handy when you want to iterate over a hashmap in the same order thats in your file.
You can use it just like a regular hashmap, but with `[{` and `}]` replacing `{` and `}`.
```
gamemodes : [{
  "pvp" : (
    ...fields...
  )
  "pve" : (
    ...fields...
  )
}]
```
boom! ordered hashmap.

Notice that sometimes we omit the `(` `)` or the `{` `}` or the `[` `]` for objects, hashmaps, and arrays respectively. This is done on purpose. As long as your data consists of a single object/map/list of objects, you do not need to explictly use the `(`/`[`/`{` notation.
i.e.
```
"red"
"yellow"
"green"
"blue"
1
2
3
4
```
is equivalent to `[ "red" "yellow" "green" "blue" 1 2 3 4 ]`
```
name : "john"
```
is equivalent to `( name : "john" )`
and
```
"name" : "john"
```
is equivalent to `{ "name" : "john" }`

## Comments
you can add comments like this:
```
/* test arc reactor on various power settings */
1 2 3 4 5
```
they can be multiline too!
```
/* test arc reactor
on various power settings */
1 2 3 4 5
```

## Multiline Strings
```
r"I am a
very cool
multiline
string"
```
note that they keep whitespace, including newline characters.
