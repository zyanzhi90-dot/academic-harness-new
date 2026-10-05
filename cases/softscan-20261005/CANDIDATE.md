# 首次问题候选：未完成独立评审

本次实际状态为 **PROBLEM_REVIEW**，还未达到人工选择交付条件。以下是首次产物的阅读入口，不构成人工选题请求。首次 JSON 为 [problems.first.json](problems.first.json)，原文未修订；完整评审交接见 [review-task.exact.txt](review-task.exact.txt)。

候选 **SOFTSCAN-SHIFT-DECISION-01**：连续软接触扫描中，超出标定条件的材料、几何、滑动阻力和接触历史变化，是否留下重要的在线法向—切向阻抗选择问题？如何在力／轨迹／脱离接触或滑移的联合目标及力矩、交互能量约束下保持实际扫描效果？保留历史 v2 的英文研究问题全文，应用为超声式机器人连续软接触扫描；未预选表示、模型、critic、MPC 或预测路线。

具体痛点是扫描跨越软硬或曲率变化、改变滑动条件、停留后重新接触时，标定条件下的阻抗最优性可能失效。实际需要继续有效扫描。**本轮没有观察到实验失效，也没有证明增益排序反转。** 候选的第一条依据是 Kong 作者明确留待后续研究的未预先辨识、突变或时变环境；其它论文提供强已有能力及各自边界。共性“决策信息不足”仅作为猜想，不另凑一个共性 failure 候选。

| 已接受证据与论文 | 已解决能力及边界 | 首次候选中的覆盖判断 |
|---|---|---|
| `j4KJ1EdUyYAJ`，Kong，Neural-Network-Based Optimal Impedance Control…，DOI `10.1109/TSMC.2025.3579017` | 预辨识软环境的标量最优阻抗；不能把它泛称为无用的无记忆模型。突变／时变参数及无预辨识是作者明确的后续方向 | IN_FIELD；PARTIAL，须检验其成熟机制能否已经解决实际任务 |
| `QPuQ4sfxSTIJ`，AuSoScan，DOI `10.1109/TMECH.2025.3583041`；`ZDySGaNsMn8J`，Deformable-Contact-Aware MPC，DOI `10.1109/TRO.2023.3286070` | 有限接触面积、局部几何／摩擦和力—运动预测控制已有真实成果；预定义阻抗不等于任务一定失败 | IN_FIELD；PARTIAL；强预测控制可能消除增益自适应的必要性 |
| `USER-TASE-2023-3282974`，Task Space Compliant Control and Six-Dimensional Force Regulation…；`USER-TRO-2022-3216078`，Choosing Stiffness and Damping… | 模型无关六维超声力调节、在线约束刚度／阻尼规划均已存在；不能主张在线增益优化本身新颖 | IN_FIELD；PARTIAL；须与充分调优的已有控制比较 |
| `U1Trzk-2GRIJ`，QP VIC，DOI `10.1109/ICRA46639.2022.9812210`；`imoj6X2imAgJ`，Deep MPVIC；`3HbLu0M801YJ`，VIC 稳定性，DOI `10.1109/TRO.2016.2593492` | 约束增益选择、学习预测和变阻抗稳定性机制已有；可执行性、接触适用条件和能量干预需逐篇区分 | IN_FIELD；PARTIAL；不是新的优化器／模块组合问题 |
| `_8NXx8-VkcgJ`、`USER-TUFFC-2011-1961`、`Ubx3Xkv4y2kJ` | 松弛、有限厚度、历史及接触力矩容量有物理依据；不同本构模型可能均有用，拟合优势不直接等于控制优势 | 支持痛点的物理可能性，未证实在线信息可辨识或收益大小 |
| `HUMAN-IJRR-2011-PSR`、`HUMAN-NEURIPS-2022-VES`、`HUMAN-MANSCI-2021-SPO` | 预测充分性、价值相关压缩、预测与决策损失差别已有理论；这些概念不能再作为新贡献 | CROSS_FIELD；PARTIAL；身份与目标物理任务覆盖分别判断 |

表内覆盖是 Main 的首次判断，尚无本次独立 Reviewer 认证。Evidence ID 对应 [EVIDENCE_REGISTRY.jsonl](../../idea-stage/EVIDENCE_REGISTRY.jsonl) 的原始内容、来源阅读记录与边界；这些是继承证据，不是本轮重新阅读的全文。

价值在于确定在线阻抗选择能否在真实变化下改善联合扫描效果，并值得额外感知、估计和计算成本。若强模型无关反馈或预定义增益的预测控制已经等效，则应承认额外增益选择没有已证实价值。单独降低力 RMSE、增加本构拟合精度或制造极少见反例不足以支持重要性；速度、轨迹、接触损失、滑移及干预成本均影响解释。

关键不确定性：痛点的实际频度／规模；安全观测能否及时区分需要不同增益的状态；能量、饱和和延迟是否主导可执行动作；优势是否只是资源／调参差异；独立扫描质量是否随控制指标改善。Mu、Wang、Guo、Qian 的决定性方法覆盖仍未关闭。本次首次候选也未逐项显式处理历史审计提到的 Beber／Xue 等集成强 prior，见另记的 [GAP_NOTES.md](GAP_NOTES.md)。因此不能据该表宣称领域没有解决方案、候选新颖性已成立或历史 failure 已改善。
