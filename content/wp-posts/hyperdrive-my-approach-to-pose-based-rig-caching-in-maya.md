Title: Hyperdrive: My approach to pose-based rig caching in Maya
Date: 2019-04-29 20:15
Author: Tim Lehr
Category: C++, Maya
Tags: C++, Caching, Maya, Plugin
Slug: hyperdrive-my-approach-to-pose-based-rig-caching-in-maya
original_url: hyperdrive-my-approach-to-pose-based-rig-caching-in-maya.html
Status: published

This blog posts covers my approaches on the topic of *posed-based rig caching*, which I prototyped as a Maya plugin during my TD studies at Filmakademie. I called this project **Hyperdrive** and recently [published the source code](https://github.com/timlehr/hyperdrive) of the most recent prototype on Github. It's heavily inspired by the pose-based rig caching solution developed and presented by Disney Animation at Siggraph 2015: ["Achieving Real-Time Playback with Production Rigs"](https://dl.acm.org/citation.cfm?id=2792519){rel="nofollow"}

Unlike common caching approaches available in DCC applications, this approach doesn't rely on time-based geometry caching. Instead it is utulizing the character rig animation values to calculate a unique pose ID, which points to a certain set of deformed character meshes stored in the cache. These poses are frame independent and can be re-used across different frame-ranges and even animation scenes.

## Caching approaches

Throughout development of the prototype, the by far most challenging aspect and most common troublemaker was the Graph Evaluation inside Maya. To tackle this issue, I tried various approaches - all within the limited access of the Maya C++ SDK - with mostly mixed results. The following paragraphs are a short breakdown of what worked, what didn't work and where the current limitations of the plugins are drawn.

### Approach 1: DG Evaluation {#id-03Hyperdrive-Summary(TL)-Approach1:DGEvaluation}

The first Hyperdrive prototype was built on the old school DG evaluation, which was still state of the art until Maya 2016 replaced it with the Evaluation Manager. DG Evaluation relies on the propagation of dirty flags from node to node. The logic is faily simple and thus, pretty easy to control. The DG prototype was a single node, which computed both pose and cache output. This node was plugged between the mesh source and the output mesh node. As a result, DG dirty propagation would always flow through the node and Hyperdrive was able to control the dirty propagation by pretending to be "clean".

However, some nodes would still execute, as complex rig setups trigger dirty propagation across thousands of nodes. To counter this, Hyperdrive would take control over the *nodeState* attribute of affected nodes and *ask* them to skip computation. This simple approach worked out quite well and saw 4-5x increases in framerate with the Ratatoskr demo scene. The DG approach also made it easy to integrate the setup into any scene and still layer nodes on top of the setup, without breaking things. However, since DG is strictly single-threaded, the performance with multiple meshes was actually much *slower* than without any caching. Another bottleneck was (and still is) the Maya viewport translation of geometry. This processing step in the viewport render pipeline can take up a lot of precious computing time, especially with bigger meshes.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/0QAQUqLyU7k?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### Approach 2: Parallel Evaluation & Custom Evaluator {#id-03Hyperdrive-Summary(TL)-Approach2:ParallelEvaluation&CustomEvaluator}

With said limitations of the DG Evaluation in mind, the way forward was clearly adapting the new *Evaluation Manager (EM)*. The EM is a complete overhaul of how Maya computes it's nodegraph. Instead of dirty propagation from back-to-front, the EM partitions the DG Graph once before evaluation start and can run the node calculation in independent *clusters*, thus enabling Parallel execution. To take advantage of this, Hyperdrive had to be restructured into two nodes: a pose node and a cache node. The pose node is responsible for hashing the animation controller values and provide a *Cache ID* to all relevant cache nodes. Since the EM Graph is calculated front-to-back, it's the only way to stop evaluation in time. Instead of *nodeState* which is not certainly stopping nodes from evaluating, the EM offers the *Frozen *attribute that is completely stopping any evaluation on the node, without the node developer taking care of implementing the mechanism. However, it became apparent that the parallelised computation makes it really hard to calculate the pose, and set the offer an updated *Frozen *value to dependent rig nodes in time. As a result, Hyperdrive caching would work as expected, but was unable to stop any evaluation in it's tracks, even if the pose was already written to cache. As a result, the playback framerate would dip drastically below what you would encounter without any caching active. So while the DG is simple enough to control, it's almost impossible to mess with the EM evaluation at runtime the same way. To counter this offer further control to developers, Autodesk provides the *Custom Evaluator API*.

An Evaluator in the EM is a Maya API class that takes control over the scheduling and partitioning of the DG into the EM Graph. It also provides the possibility to run code *before* or *after* a frame was completely evaluated. The Hyperdrive Evaluator takes advantage of this an positions itself as the Evaluator with the highest priority, thus getting access to the EM before any other code does. It then computes the Pose IDs for all pose nodes in the scene and checks if all relevant cache nodes have a corresponding cache. If all poses are available in the cache, Hyperdrive stops evaluation for all nodes - except it's own pose / cache nodes, as well as the output meshes of the character. Unfortunately, this operation is still single threaded, so the amount of Hyperdrive rigs in the scene greatly increases it's computational time.

The Evaluator has another major drawback for Hyperdrive: A version of the evaluator which stops evaluation just on certain nodes and their history proved to be very ineffective, since complex rigs still evaluate a ton of nodes, and it's impossible to pinpoint all the computational intensive nodes without resorting to a huge amount of manual labor. As a result the current prototype relies on stopping all node computation in the scene and whitelisting certain nodes if needed. This gives similar performance results to DG with about 4-5x speedup, while still being able to compute multiple mesh caches (in parallel), something that is unfeasible in DG. The ugly side effect of this radical approach is that unrelated animated nodes in the scene need to be whitelisted in order to compute at all while Hyperdrive is active.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/2I8lYrASROI?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Conclusion

My research has proven it's possible to replicate a pose-based caching setup within Autodesk Maya. However, each approach I tried has it's own set of pitfalls making it unsuitable for productions. The first prototype using the classic DG evaluation approach yielded the most reliable results with little setup overhead. However, given the complexity of modern character rigs, it's single threaded nature limits the use-cases. The parallel prototype is much more flexible and able to compute nodes in parallel, but it's also very hard to skip the necessary evaluation steps without breaking the scene. It's results with Hyperdrive are more opaque than the output of DG, even though the tools to control it are much better.

To make the system suitable for production, easier profiling tools and an even more low-level Evaluation API would be needed. The second bottleneck, slow mesh drawing on the GPU, can't be fixed with any Maya functionality and would require direct OpenGL drawing of the cached geometry, bypassing any further Maya processing (like Disney does). This would require a lot of work, as all the viewport interaction needs to be replicated.

For productions going forward, a switch to Maya 2019 is recommendable. The latest version of the application comes with brand new caching functionality, allowing Maya to cache the graph evaluation in a background thread and only re-cache invalid frame ranges. This still doesn't quite have the same effect as a pose based approach which is completely independent of time and animation scenes, but it gives the animator consistent playback speed with an interactive viewport.