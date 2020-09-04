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
[ 1 2 3 4 5 ]
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
[ [ "hello" ] [ "world" ] ]
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
