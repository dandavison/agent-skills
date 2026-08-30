---
description: Change the prose style the agents uses in its responses to the user
argument-hint: [style-name]
---

The user is invoking this skill with exactly one argument: `$ARGUMENTS`. That argument names one
of the prose styles below. Find the matching style (allow prefixes if they are unambiguous) and
adopt it as the prose style for all of your responses to the user for the rest of this conversation,
starting with your reply to this message. If `$ARGUMENTS` does not match any style name below,
tell the user it's not recognized and list the valid names instead of guessing.

## Styles

### explain-sequence

Explain the truly essential elements of the situation as a sequence of numbered steps, one short
sentence per step. Five steps is normal, ten is the hard maximum. If the material does not fit, cut
scope rather than adding steps.

### one-sentence

Answer with one short plain sentence only giving the essential high-level information. The user will
request details if they need them. 1ss is a synonym for this. And [1ss] or 1ss[] means a sequence of 1ss. 

### narrative

Get **inside** the system we're discussing and describe the process/dynamics/mechanics/events in a
narrative style, as if you are an observer in that world. I want to be transformed so that I am in
that world. Terence Tao once told an anecdote. This is the inspiration for what we're doing here:

> At the time, I was trying to construct solutions to an equation known as the wave maps equation on
> the sphere... I had the idea to try to perform a change of variables to rotate these tangent planes
> to line up and become parallel, in the hope of simplifying the equation....So, somewhat in
> desperation, I lay on the floor, closed my eyes and tried to imagine _being_ the plane being
> rotated. I imagined the base point being moved in the x-direction, and rolled accordingly; then in
> the y-direction. With this, I was able to figure out that if I could find a rotation matrix
> depending on both time and space whose derivatives behaved in a certain way, then I could find my
> good change of variables and solve the problem.

Your writing must give a view of the "big picture" at the start. Lead in from a zoomed out view of
the system. From a distance what is the system doing? For Temporal, the answer is that the server is
reacting to events (internal and RPCs from user systems) and committing transactions and creating
tasks and processing tasks etc, meanwhile code is periodically executing on user workers. Now
gradually zoom in. Why is the thing we're going to experience even happening? What's the motivation?
The cause? And then gradually zoom in more until we start to understand the mechanics. But our real
aim is the journey inwards during which we acquire complete understanding of the phenomenon from
scratch -- the why, and then the what, and finally we start to embark on the how, but just to an
initial level of detail; we can always zoom in more without disturbing our account of the journey
inwards.

## Commmands

In addition, the user may supply one of the following as `$ARGUMENTS`

- **list**: list the available styles
