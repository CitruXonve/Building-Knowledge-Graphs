#### Task 2.2.1

Formal definition:
> A mad cow is a cow that has been eating the brains of sheep.

Explanation in other words:
> Mad cow is a subclass of cow under vegetarian animal category that eats brains, which are parts of sheep.

#### Task 2.2.2

Inherited constraints from superclass `cow`:

> animal  
>    and (eats only (not (animal)))  
>    and (eats only (not (part_of some animal)))  
> eats some owl:Thing

The problem is that definition contradicts with such constraints, because `brain` is actually part of `sheep` animal according to the definition, which violates `(eats only (not (part_of some animal)))`.

#### Task 2.3.1

`Mad cow` becomes the only subclass of `owl:Nothing` afterwards, but wasn't before using reasoner.

#### Task 2.3.2

`Giraffe` becomes a subclass of `vegetarian` and inherits the constraints from `vegetarian` after using reasoner.

#### Task 2.3.3

Before using reasoner, `Tom` is only `owl:Thing` and `Minnie` is an `elderly` `femail`.  Afterwards, `Tom ` is also a `cat` `pet` and `Minnie` also becomes an `old lady`.

#### Task 2.3.4

|Not using reasoner|Using reasoner|Reason|
|---|---|---|
|Fred   |Fred   |(none)|
|Joe    |Joe    |(none)|
|Kevin  |Kevin  |(none)|
|Walt   |Mick   |(none)|
|(none)|Minnie |Becomes an `old lady`, which is a subclass of `person`|
|(none)|Pete   |Becomes a `pet owner`, which is a subclass of `person`|
|(none)|Walt   |Becomes an `animal lover`, which is a subclass of `person`|
||||


No one was added.

#### Task 2.3.5

`Mick` is originally a `male`. Afterwards, `Mick` is a white van man owning a dog.  
`Daily Mirror` is just an `owl:Thing` and then also becomes a `tabloid`.

#### Task 2.3.6


|pet owner|
|---|
|Fred   |
|Joe    |
|Kevin  |
|Mick   |
|Minnie |
|Pete   |
|Walt   |
||

#### Task 2.3.7

A `person` must have at least 3 `pets` to be an `animal lover`.

#### Task 2.3.8

All the `pets` of an `animal lover` must be `animals`, because the range of `has_pet` is `animal`.  
An `old lady` need to be a `person` because the domain of `has_pet` is `person`.