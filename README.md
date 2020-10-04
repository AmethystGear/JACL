# JACL <img src="https://user-images.githubusercontent.com/21998904/92298114-79262880-eefa-11ea-98e6-ba114050e75c.png" width="40">
Just Another Configuration Language



Basically what the title says, more or less.

For some reason, lots of people love using JSON as a configuration format. Which sucks. For a number of reasons, including:
1. No comments in JSON (Seriously, you'd think this would need to be the only one on the list.)
2. Everything needs to be a hashmap (with string keys... ew)
3. No trailing commas (sucks when you're trying to hand roll it out)
4. No multiline strings

and many more!

Yeah, you could use YAML or XML, but those have their own problems. JSON syntax feels like it's 80% of the way to a config format. So why not make something that borrows from JSON syntax, but fixes a lot of the problems?

Enter JACL. JACL is a superset of JSON that fixes most of JSON's problems (for configs)! Since it's a strict superset, you can plug your JSON right into JACL. We wont mind!

## Hello JACL
Let's start with the most basic config file possible:
```
0
```
-- this would be the integer 0

In JACL, any primitive or collection sitting alone in a file is 100% ok. That means i can do:
```
"hello world"
```
-- this would be the string "hello world"

or
```
1 2 3 4 5
```
-- this would be a list containing 1, 2, 3, 4, and 5

Note the lack of commas. That's right, you won't be needing commas anymore. JSON trailing comma errors begone!

This isn't to say that you *can't* have commas, JACL is a superset of JSON, so commas are allowed. JACL simply doesn't *require* commas like JSON, so you don't have to use them if you don't want to.
As such, this is valid JACL:
```
1,2,3,4,5
```
so is this:
```
1,2,3,4,5,
```
so is this:
```
1,     2, 3,    4,5,
```

But what if I want to name my data? Well, there are two ways you can go about this.
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
// test arc reactor on various power settings
1 2 3 4 5
```
they can be multiline too!
```
/* test arc reactor
on various power settings 
I made my list explicit for fun
in this example */
[ 1 2 3 4 5 ]
```

## Multiline Strings
```
"I am a
very cool
multiline
string"
```
note that they keep whitespace, including newline characters.
