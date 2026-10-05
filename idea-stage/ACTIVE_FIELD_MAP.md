# Active Field Map

coverage_status: SUFFICIENT
coverage_record:
research_effort_budget: {"completed_query_events": 49, "completed_read_events": 99, "canonical_decision_grade_evidence_cards": 82, "active_continuation_subset_completed": 19, "new_read_events_in_continuation": 0}
stopping_reason: The continuation reused all 99 verified read events and converted the complete 19-paper active subset into canonical decision-grade Evidence Cards, yielding 82 canonical cards. The added primary evidence materially extends the accepted taxonomy with constrained QP/MPC and SCBF predictive impedance, energy-aware predefined-time interaction, hierarchical and diffusion skill learning, human-intent adaptation, multi-objective phase stiffness learning, and physical-prior learned dynamics compensation. Four foundational or review sources are used only for taxonomy and lineage with explicit review-level epistemic boundaries. Remaining questions are now specific research problems rather than top-level landscape coverage deficits, so broader searching is unlikely to reorganize the map before problem generation.

## Field Core Purposes

```json
[
  "Regulate the mechanical relation between robot motion and interaction force at a power port rather than command either variable in isolation.",
  "Maintain useful compliant behavior across free motion, impact, sustained contact and release.",
  "Choose or adapt impedance to trade tracking, force regulation, task success, robustness and human effort for the current context.",
  "Preserve analyzable coupled stability, passivity or safe-set invariance when impedance varies, optimization or learning is introduced, and control is implemented on sampled hardware."
]
```

## Typical Tasks And Scenarios

```json
[
  "Free-to-contact transitions, surface following, wiping, polishing, ultrasound and constrained manipulation",
  "Assembly, insertion, door opening, sequential contact skills and uncertain-geometry manipulation",
  "Interaction with unknown stiffness, damping, contact location, friction, payload or human guidance",
  "Flexible-joint, series-elastic and torque-controlled collaborative robots",
  "Repeated-task, demonstration-driven, reinforcement, diffusion and Bayesian impedance learning",
  "Obstacle avoidance and workspace constraints under impedance control"
]
```

## Core Bottlenecks

```json
[
  {
    "id": "B1_IMPEDANCE_SELECTION",
    "name": "Context-dependent impedance selection",
    "description": "Classical realization does not determine inertia, damping, stiffness, equilibrium or their state dependence; adaptive and learned solutions inherit objectives, priors and data distributions."
  },
  {
    "id": "B2_CONTACT_TRANSITION",
    "name": "Contact-transition stability",
    "description": "Stable in-contact equilibrium does not ensure capture after impact; collision state, environment stiffness, damping, delay and bandwidth determine rebound and peak force."
  },
  {
    "id": "B3_REALIZATION_ROBUSTNESS",
    "name": "Desired-versus-realized impedance",
    "description": "Robot dynamics, friction, payload, sensing, sampling, delay, saturation and inner loops distort the commanded port behavior."
  },
  {
    "id": "B4_VARIABLE_GAIN_ENERGY",
    "name": "Energy injection by variable gains",
    "description": "Time- or state-varying stiffness can inject energy; arbitrary schedules do not inherit fixed-gain passivity."
  },
  {
    "id": "B5_LEARNING_GENERALIZATION",
    "name": "Learning efficiency and generalization",
    "description": "Learning remains tied to repeated tasks, demonstrations, hand-designed rewards, tuned primitives, selected geometries or simulator distributions."
  },
  {
    "id": "B6_CERTIFICATE_REALITY_GAP",
    "name": "Certificate-to-hardware gap",
    "description": "Continuous-time proofs and model safe sets do not automatically cover discretization, filtering, infeasibility, solver overruns, saturation, collision injury or standards compliance."
  },
  {
    "id": "B7_REPRESENTATION_SENSING",
    "name": "Representation and sensing",
    "description": "Joint/task space, impedance/admittance causality, force sensing, learned residuals and energy representations trade observability, transfer, expressiveness and certifiability."
  },
  {
    "id": "B8_COMPLEX_CONTACT",
    "name": "Complex and multi-contact extension",
    "description": "Rigid low-dimensional results do not transfer automatically to flexible, redundant, nonlinear, active-human, moving-obstacle and multi-contact systems."
  },
  {
    "id": "B9_OBJECTIVE_SAFETY_GAP",
    "name": "Objective and safety-evidence gap",
    "description": "Low force, compliance proxies, success-conditioned statistics and composite rewards are not equivalent to passivity, coupled stability, injury safety or deployment certification."
  }
]
```

## Method Families

```json
[
  {
    "id": "M1_CLASSICAL_PORT_REALIZATION",
    "name": "Classical port impedance and admittance",
    "core_mechanism": "Specify a force–motion relation, choose causal realization and map it through robot mechanics and inner loops."
  },
  {
    "id": "M2_CONTACT_TRANSITION_DESIGN",
    "name": "Contact-transition design",
    "core_mechanism": "Choose inertia, damping, stiffness and bandwidth from unilateral-contact and delayed-interaction models."
  },
  {
    "id": "M3_ROBUST_ADAPTIVE_REALIZATION",
    "name": "Robust and adaptive realization",
    "core_mechanism": "Compensate uncertain robot/environment dynamics while attempting to preserve a prescribed impedance or force objective."
  },
  {
    "id": "M4_FLEXIBLE_JOINT_PASSIVITY",
    "name": "Flexible-joint and compliant-actuation impedance",
    "core_mechanism": "Exploit physical elasticity and nested torque/impedance loops with passivity-aware design."
  },
  {
    "id": "M5_ITERATIVE_DEMONSTRATION_OPTIMIZATION",
    "name": "Iterative, demonstration and multi-objective impedance learning",
    "core_mechanism": "Learn repeated-task input or phase-wise gains from trials/demonstrations and explicit task–compliance objectives."
  },
  {
    "id": "M6_ENERGY_PASSIVITY_FILTERS",
    "name": "Energy tanks and passivity filters",
    "core_mechanism": "Track available energy or reshape gain-dependent power so variable impedance respects a conditional passive mapping."
  },
  {
    "id": "M7_IMPEDANCE_STRUCTURED_RL",
    "name": "Impedance-structured RL and skill policies",
    "core_mechanism": "Learn motion, primitive selection and impedance actions while a faster classical controller realizes the policy."
  },
  {
    "id": "M8_ENERGY_STRUCTURED_LEARNING",
    "name": "Energy-structured learned impedance",
    "core_mechanism": "Constrain learned force fields to gradients of valid energy functions so nominal stability/passivity follows by construction."
  },
  {
    "id": "M9_ADAPTIVE_OPTIMAL_SELECTION",
    "name": "Adaptive and optimal target-impedance selection",
    "core_mechanism": "Adapt selected gains from force error or solve an explicit tracking–force optimal-control objective."
  },
  {
    "id": "M10_CONSTRAINED_PREDICTIVE_IMPEDANCE",
    "name": "QP/MPC constrained predictive impedance",
    "core_mechanism": "Optimize impedance and complementary actions online under impedance, state or SCBF safe-set constraints."
  },
  {
    "id": "M11_HUMAN_INTENT_SKILL_LEARNING",
    "name": "Human-intent and tactile-skill adaptation",
    "core_mechanism": "Infer intention or physically adapt motion/force skills while modulating impedance and optionally bounding task energy."
  },
  {
    "id": "M12_LEARNED_DYNAMICS_COMPENSATION",
    "name": "Learned dynamics and uncertainty compensation",
    "core_mechanism": "Combine physical robot models, observers and neural residuals to improve low-gain impedance realization without claiming the learner itself is a stability certificate."
  }
]
```

## Family Development Traces

```json
[
  {
    "transition_id": "T1_PORT_TO_CAUSAL_REALIZATION",
    "family": "M1_CLASSICAL_PORT_REALIZATION",
    "previous_problem_or_bottleneck": "Separate motion and force control ignored the energetic loading created by the environment.",
    "progress_and_conditions": "Port impedance/admittance and passive interconnection theory supplied exact causal and coupled-stability language under power-conjugate, mostly linear one-port assumptions.",
    "residual_or_new_bottleneck": "Hardware causality, inner-loop dynamics, sampling and active or multi-contact environments limit ideal results.",
    "research_question_shift": "The question shifted from isolated tracking stability to which port behavior can be physically realized and remain stable when coupled.",
    "subsequent_direction": "Hardware-aware admittance/impedance realization, compliant actuation and implementation-level passivity.",
    "transition_problem_status": "mature_under_specific_conditions",
    "evidence_ids": [
      "y051Shzv2A8J",
      "5peSBIP--BgJ",
      "B68ZOyQGJ80J"
    ]
  },
  {
    "transition_id": "T2_FIXED_TO_VARIABLE_ENERGY",
    "family": "M6_ENERGY_PASSIVITY_FILTERS",
    "previous_problem_or_bottleneck": "Fixed gains could not reconcile changing precision and compliance requirements.",
    "progress_and_conditions": "Rate conditions, energy tanks, deflection-domain observers and task-energy shaping exposed and bounded gain-induced power under controller-specific assumptions.",
    "residual_or_new_bottleneck": "Energy-budget selection, sampled implementation, discontinuous policies, near-zero-velocity sensitivity and nonpassive environments remain unresolved.",
    "research_question_shift": "The question moved from whether a fixed impedance is passive to how online adaptation may spend or dissipate energy.",
    "subsequent_direction": "Less conservative passivity filters jointly designed with learning and contact constraints.",
    "transition_problem_status": "partially_addressed",
    "evidence_ids": [
      "B68ZOyQGJ80J",
      "pO9mjm67fekJ",
      "JKrA-rLcvHkJ",
      "Qm5BKnMez5cJ"
    ]
  },
  {
    "transition_id": "T3_ROBUST_TO_LEARNED_REALIZATION",
    "family": "M12_LEARNED_DYNAMICS_COMPENSATION",
    "previous_problem_or_bottleneck": "Model error and friction required high feedback gains that reduced compliance.",
    "progress_and_conditions": "Adaptive observers, fuzzy/neural compensation and physical-prior recurrent residual models improved tested tracking or boundedness under selected uncertainties.",
    "residual_or_new_bottleneck": "Learned residual extrapolation, payload shift, contact torque, sensor dependence and full-loop passivity are not certified.",
    "research_question_shift": "The focus shifted from estimating a compact uncertainty to learning history-dependent residual dynamics without losing physical structure.",
    "subsequent_direction": "Constraint-aware residual learning with online distribution-shift detection and energetic closed-loop analysis.",
    "transition_problem_status": "partially_addressed",
    "evidence_ids": [
      "Rw7RRyHn644J",
      "gFUzDeNXl9cJ",
      "NmJOT6QG-tUJ"
    ]
  },
  {
    "transition_id": "T4_ITERATIVE_TO_GENERATIVE_SKILLS",
    "family": "M5_ITERATIVE_DEMONSTRATION_OPTIMIZATION",
    "previous_problem_or_bottleneck": "Repeated-task learning improved fixed horizons but transferred poorly and left impedance objectives hand chosen.",
    "progress_and_conditions": "Sparse-GP iteration, impedance-aware segmentation with multi-objective BO and diffusion-based skill generation learned richer time/state-dependent behavior on selected tasks.",
    "residual_or_new_bottleneck": "Early-trial safety, data cost, manually chosen objectives/segments, nonpassive stiffness increases and cross-task transfer remain open.",
    "research_question_shift": "The question shifted from improving a repeated input to learning structured, multimodal compliant skill distributions and Pareto choices.",
    "subsequent_direction": "Safe generative skill learning with explicit energy and failure-aware objectives.",
    "transition_problem_status": "partially_addressed",
    "evidence_ids": [
      "nZ1L1Vl7KvEJ",
      "NeHbiasbAqAJ",
      "kexwZicrUfAJ"
    ]
  },
  {
    "transition_id": "T5_RL_ACTION_TO_SEQUENTIAL_POLICY",
    "family": "M7_IMPEDANCE_STRUCTURED_RL",
    "previous_problem_or_bottleneck": "Flat RL impedance actions handled short tasks but required extensive exploration and provided weak long-horizon composition.",
    "progress_and_conditions": "Asymmetric impedance policies and hierarchical impedance primitives improved tested insertion, wiping and sequential manipulation success, including limited sim-to-real transfer.",
    "residual_or_new_bottleneck": "Different rewards, success-conditioned force metrics, tuned primitives, small physical samples and absent passivity weaken safety and superiority claims.",
    "research_question_shift": "The emphasis moved from choosing a gain vector to composing compliant skills and adapting directional stiffness over task phases.",
    "subsequent_direction": "Failure-inclusive evaluation and certificate-constrained hierarchical or generative policies.",
    "transition_problem_status": "partially_addressed",
    "evidence_ids": [
      "VewJDUrPRiAJ",
      "lkDBxoBPKI8J",
      "kexwZicrUfAJ"
    ]
  },
  {
    "transition_id": "T6_OPTIMAL_TO_CONSTRAINED_PREDICTION",
    "family": "M10_CONSTRAINED_PREDICTIVE_IMPEDANCE",
    "previous_problem_or_bottleneck": "Optimal impedance selection often ignored state, impedance and workspace constraints or reacted only after risk emerged.",
    "progress_and_conditions": "Coupled QPs, MPC and linearized SCBFs optimized impedance and complementary actions; selected experiments demonstrated bounded gains, reduced violations and anticipatory obstacle avoidance.",
    "residual_or_new_bottleneck": "Recursive feasibility, model/force prediction error, moving obstacles, worst-case solve time and the distinction between safe-set invariance and injury safety remain.",
    "research_question_shift": "The question shifted from which impedance minimizes a cost to which feasible impedance trajectory preserves task and modeled safety constraints online.",
    "subsequent_direction": "Robust/stochastic predictive impedance with formal discrete-time feasibility and collision-risk semantics.",
    "transition_problem_status": "partially_addressed",
    "evidence_ids": [
      "U1Trzk-2GRIJ",
      "ctEq_owme9kJ",
      "xlNjdqnC2fMJ"
    ]
  },
  {
    "transition_id": "T7_PREDICTION_TO_PREDEFINED_TIME",
    "family": "M10_CONSTRAINED_PREDICTIVE_IMPEDANCE",
    "previous_problem_or_bottleneck": "Conservative safety impedance could miss explicit task deadlines, while aggressive convergence could increase force or velocity.",
    "progress_and_conditions": "Time scaling plus energy-aware predictive control and learned meta-parameter tuning achieved reported predefined-time errors and higher composite reward in tested disturbances.",
    "residual_or_new_bottleneck": "Composite reward hides tradeoffs, tuning does not prove passivity, and the human-arm case lacks repeatability and clinical or standards validation.",
    "research_question_shift": "The objective expanded from constraint satisfaction to jointly controlling convergence deadline, force overshoot and velocity.",
    "subsequent_direction": "Multi-objective deadline-aware control with separately auditable safety outcomes.",
    "transition_problem_status": "partially_addressed",
    "evidence_ids": [
      "4tr9C5LNwYwJ",
      "ctEq_owme9kJ"
    ]
  },
  {
    "transition_id": "T8_HUMAN_GUIDANCE_TO_INTENT_ADAPTATION",
    "family": "M11_HUMAN_INTENT_SKILL_LEARNING",
    "previous_problem_or_bottleneck": "Human guidance required either fixed impedance or manual post-processing and did not directly express changing intent.",
    "progress_and_conditions": "sEMG intention adaptation and passivity-oriented tactile-skill shaping reduced reported effort/force or enabled autonomous replay on prescribed tasks.",
    "residual_or_new_bottleneck": "User variability, fixed trajectories, energy-limit selection, participant statistics, transient force and universal safety remain unresolved.",
    "research_question_shift": "The question shifted from compliant guidance to how intention and physically adapted skills should modulate impedance online.",
    "subsequent_direction": "User-independent intent models coupled to energy and bandwidth-aware adaptation.",
    "transition_problem_status": "partially_addressed",
    "evidence_ids": [
      "3kL0MPf4EmMJ",
      "JKrA-rLcvHkJ"
    ]
  },
  {
    "transition_id": "T9_PASSIVITY_TO_MULTIPLE_SAFETY_NOTIONS",
    "previous_problem_or_bottleneck": "The literature often used compliance, passivity, boundedness and obstacle avoidance interchangeably as safety evidence.",
    "progress_and_conditions": "Recent work distinguishes interaction-port passivity, conditional boundedness/GAS, SCBF forward invariance, impedance limits and empirical low-force behavior.",
    "residual_or_new_bottleneck": "No single property covers human injury, solver failure, active environments, perception faults and standards compliance.",
    "research_question_shift": "The field must state which safety property is proved, for which port/set/model, and which deployment hazard remains untested.",
    "subsequent_direction": "Layered assurance linking energetic, geometric, control-computation and human-outcome evidence.",
    "transition_problem_status": "reframed",
    "evidence_ids": [
      "pO9mjm67fekJ",
      "ctEq_owme9kJ",
      "lkDBxoBPKI8J",
      "y051Shzv2A8J"
    ]
  }
]
```

## Problem Method Matrix

```json
[
  {
    "problem": "B1_IMPEDANCE_SELECTION",
    "method": "M5_ITERATIVE_DEMONSTRATION_OPTIMIZATION",
    "relationship": "Optimizes phase/trial gains against supplied task and compliance objectives."
  },
  {
    "problem": "B1_IMPEDANCE_SELECTION",
    "method": "M7_IMPEDANCE_STRUCTURED_RL",
    "relationship": "Learns state-conditioned impedance from rewards but inherits exploration and reward validity."
  },
  {
    "problem": "B2_CONTACT_TRANSITION",
    "method": "M2_CONTACT_TRANSITION_DESIGN",
    "relationship": "Directly analyzes capture and contact maintenance."
  },
  {
    "problem": "B3_REALIZATION_ROBUSTNESS",
    "method": "M3_ROBUST_ADAPTIVE_REALIZATION",
    "relationship": "Compensates structured uncertainty around a desired impedance."
  },
  {
    "problem": "B3_REALIZATION_ROBUSTNESS",
    "method": "M12_LEARNED_DYNAMICS_COMPENSATION",
    "relationship": "Improves low-gain tracking empirically while adding distribution-shift risk."
  },
  {
    "problem": "B4_VARIABLE_GAIN_ENERGY",
    "method": "M6_ENERGY_PASSIVITY_FILTERS",
    "relationship": "Accounts for or restricts gain-induced power."
  },
  {
    "problem": "B4_VARIABLE_GAIN_ENERGY",
    "method": "M8_ENERGY_STRUCTURED_LEARNING",
    "relationship": "Constrains learned forces to valid potentials."
  },
  {
    "problem": "B5_LEARNING_GENERALIZATION",
    "method": "M7_IMPEDANCE_STRUCTURED_RL",
    "relationship": "Broadens policies but remains task/distribution dependent."
  },
  {
    "problem": "B5_LEARNING_GENERALIZATION",
    "method": "M11_HUMAN_INTENT_SKILL_LEARNING",
    "relationship": "Adapts to guidance or intent but remains user- and protocol-dependent."
  },
  {
    "problem": "B6_CERTIFICATE_REALITY_GAP",
    "method": "M10_CONSTRAINED_PREDICTIVE_IMPEDANCE",
    "relationship": "Adds modeled constraints but requires feasible, timely and accurate prediction."
  },
  {
    "problem": "B7_REPRESENTATION_SENSING",
    "method": "M1_CLASSICAL_PORT_REALIZATION",
    "relationship": "Causality and hardware determine sensing and inner-loop requirements."
  },
  {
    "problem": "B7_REPRESENTATION_SENSING",
    "method": "M12_LEARNED_DYNAMICS_COMPENSATION",
    "relationship": "Uses physical priors and memory but adds latent-state and training-data dependence."
  },
  {
    "problem": "B8_COMPLEX_CONTACT",
    "method": "M4_FLEXIBLE_JOINT_PASSIVITY",
    "relationship": "Extends port design to elastic transmissions under model boundaries."
  },
  {
    "problem": "B9_OBJECTIVE_SAFETY_GAP",
    "method": "M10_CONSTRAINED_PREDICTIVE_IMPEDANCE",
    "relationship": "Makes geometric/state constraints explicit but does not cover every physical hazard."
  },
  {
    "problem": "B9_OBJECTIVE_SAFETY_GAP",
    "method": "M5_ITERATIVE_DEMONSTRATION_OPTIMIZATION",
    "relationship": "Exposes Pareto tradeoffs but compliance proxies remain distinct from safety outcomes."
  }
]
```

## Assumption Effectiveness Failure Matrix

```json
[
  {
    "family": "M1_CLASSICAL_PORT_REALIZATION",
    "assumptions": [
      "Power-conjugate ports",
      "Adequate inner loops"
    ],
    "effective": [
      "Known target impedance and compatible hardware"
    ],
    "failure": [
      "Sampling, delay, active or multi-contact environment"
    ],
    "source_ids": [
      "y051Shzv2A8J",
      "5peSBIP--BgJ"
    ]
  },
  {
    "family": "M2_CONTACT_TRANSITION_DESIGN",
    "assumptions": [
      "Bounded contact model and delay"
    ],
    "effective": [
      "Analyzed unilateral contact regime"
    ],
    "failure": [
      "Unknown collision energy or multiple contacts"
    ],
    "source_ids": [
      "D0Bq_8tYnBQJ",
      "bh9zIsh1OIgJ"
    ]
  },
  {
    "family": "M3_ROBUST_ADAPTIVE_REALIZATION",
    "assumptions": [
      "Structured bounded uncertainty"
    ],
    "effective": [
      "Estimator dynamics match uncertainty timescale"
    ],
    "failure": [
      "Fast contact change, noise or saturation"
    ],
    "source_ids": [
      "03NKTnfzQ6sJ",
      "Rw7RRyHn644J"
    ]
  },
  {
    "family": "M4_FLEXIBLE_JOINT_PASSIVITY",
    "assumptions": [
      "Known elastic transmission and torque loop"
    ],
    "effective": [
      "Passive modeled contact"
    ],
    "failure": [
      "Nonlinear elasticity or unmodeled sensing dynamics"
    ],
    "source_ids": [
      "ioYGUCT49JIJ",
      "Qm5BKnMez5cJ"
    ]
  },
  {
    "family": "M5_ITERATIVE_DEMONSTRATION_OPTIMIZATION",
    "assumptions": [
      "Repeatability or informative demonstrations",
      "Valid objectives"
    ],
    "effective": [
      "Finite-horizon selected tasks"
    ],
    "failure": [
      "Early unsafe trials, objective mismatch, cross-task shift"
    ],
    "source_ids": [
      "nZ1L1Vl7KvEJ",
      "NeHbiasbAqAJ"
    ]
  },
  {
    "family": "M6_ENERGY_PASSIVITY_FILTERS",
    "assumptions": [
      "Correct energy bookkeeping",
      "Passive port/environment conditions"
    ],
    "effective": [
      "Continuous scheduled gains in tested regime"
    ],
    "failure": [
      "Discontinuity, budget misselection, sampled saturation"
    ],
    "source_ids": [
      "pO9mjm67fekJ",
      "JKrA-rLcvHkJ"
    ]
  },
  {
    "family": "M7_IMPEDANCE_STRUCTURED_RL",
    "assumptions": [
      "Representative rewards and training distribution"
    ],
    "effective": [
      "Selected contact tasks with fast low-level control"
    ],
    "failure": [
      "Rare failures, reward shift, unsafe exploration"
    ],
    "source_ids": [
      "VewJDUrPRiAJ",
      "lkDBxoBPKI8J"
    ]
  },
  {
    "family": "M8_ENERGY_STRUCTURED_LEARNING",
    "assumptions": [
      "Exact model and valid positive energy representation"
    ],
    "effective": [
      "Representable conservative force fields"
    ],
    "failure": [
      "Discrete realization, saturation or insufficient expressiveness"
    ],
    "source_ids": [
      "kQorDN4oymIJ",
      "3HbLu0M801YJ"
    ]
  },
  {
    "family": "M9_ADAPTIVE_OPTIMAL_SELECTION",
    "assumptions": [
      "Correct cost and environment class"
    ],
    "effective": [
      "Structured force-tracking optimization"
    ],
    "failure": [
      "Nonlinear changing environments or unsafe excitation"
    ],
    "source_ids": [
      "d1A3Ar8wid4J",
      "tS1rA372YsUJ"
    ]
  },
  {
    "family": "M10_CONSTRAINED_PREDICTIVE_IMPEDANCE",
    "assumptions": [
      "Accurate prediction and feasible timely QP"
    ],
    "effective": [
      "Modeled bounds, obstacles and horizons"
    ],
    "failure": [
      "Model mismatch, infeasibility, moving uncertainty, overruns"
    ],
    "source_ids": [
      "U1Trzk-2GRIJ",
      "ctEq_owme9kJ",
      "4tr9C5LNwYwJ"
    ]
  },
  {
    "family": "M11_HUMAN_INTENT_SKILL_LEARNING",
    "assumptions": [
      "Reliable intent/interaction sensing"
    ],
    "effective": [
      "Calibrated users and prescribed skills"
    ],
    "failure": [
      "User variability, fatigue, bandwidth or unselected energy limits"
    ],
    "source_ids": [
      "3kL0MPf4EmMJ",
      "JKrA-rLcvHkJ"
    ]
  },
  {
    "family": "M12_LEARNED_DYNAMICS_COMPENSATION",
    "assumptions": [
      "Training covers deployment dynamics",
      "Fast inference"
    ],
    "effective": [
      "Same-robot low-gain tracking and bounded uncertainty"
    ],
    "failure": [
      "Payload/contact shift, latent-state error, learner extrapolation"
    ],
    "source_ids": [
      "NmJOT6QG-tUJ",
      "gFUzDeNXl9cJ",
      "Rw7RRyHn644J"
    ]
  }
]
```

## Consensus

```json
[
  "Impedance control is fundamentally a port-behavior problem; isolated tracking stability is insufficient for energetic interaction.",
  "Impedance/admittance causality, robot hardware and inner-loop dynamics materially constrain realizable behavior.",
  "Variable stiffness can inject energy, so learning or scheduling gains requires explicit stability/passivity treatment when such guarantees are claimed.",
  "Learning improves selected task performance and adaptation, but guarantees usually come from surrounding model, energy or constraint structure rather than the learned optimizer itself.",
  "Compliance, low measured force, boundedness, passivity, safe-set invariance and human safety are distinct evidence claims.",
  "Most modern results remain platform-, task-, model- and distribution-specific; broad deployment conclusions require failure-inclusive physical evaluation."
]
```

## Unresolved Contradictions

```json
[
  "Higher stiffness improves precision and task completion but can increase interaction energy and force; no universal schedule resolves the tradeoff.",
  "Passivity offers environment-robust coupled stability yet can be conservative; predictive and learning methods improve performance while adding model and computation dependence.",
  "Low successful-trial force is reported as safer behavior, but excluding failures can hide the force exposure most relevant to safety.",
  "Physical priors improve learned-model generalization, but physical consistency of one component does not certify the complete learned feedback loop.",
  "SCBF forward invariance and predefined-time convergence are formal properties of modeled systems, not direct evidence of injury avoidance or standards compliance."
]
```

## Coverage Record

```json
{
  "coverage_status": "SUFFICIENT",
  "research_effort_budget": {
    "completed_query_events": 49,
    "completed_read_events": 99,
    "canonical_decision_grade_evidence_cards": 82,
    "active_continuation_subset_completed": 19,
    "new_read_events_in_continuation": 0
  },
  "stopping_reason": "The continuation reused all 99 verified read events and converted the complete 19-paper active subset into canonical decision-grade Evidence Cards, yielding 82 canonical cards. The added primary evidence materially extends the accepted taxonomy with constrained QP/MPC and SCBF predictive impedance, energy-aware predefined-time interaction, hierarchical and diffusion skill learning, human-intent adaptation, multi-objective phase stiffness learning, and physical-prior learned dynamics compensation. Four foundational or review sources are used only for taxonomy and lineage with explicit review-level epistemic boundaries. Remaining questions are now specific research problems rather than top-level landscape coverage deficits, so broader searching is unlikely to reorganize the map before problem generation.",
  "coverage_gaps": []
}
```

## Unresolved Problem Leads

```json
[
  "Discrete-time, solver-aware passivity and feasibility for learned or predictive variable impedance under saturation and delay.",
  "Layered assurance connecting port passivity, geometric safe sets, computation timing, force limits and human-outcome evidence.",
  "Failure-inclusive benchmarks that report force/energy for unsuccessful as well as successful trials.",
  "Safe generative and hierarchical impedance policies with cross-task transfer and explicit energy budgets.",
  "Online detection of payload, contact and user distribution shift for learned dynamics or intent models.",
  "Automatic selection of energy limits, Pareto objectives, segment counts and impedance parameterizations without unsafe on-robot search.",
  "Moving-obstacle, active-human, nonlinear and multi-contact validation beyond rigid low-dimensional models.",
  "Human-subject protocols with participant counts, uncertainty estimates and clinically or industrially meaningful safety outcomes."
]
```
