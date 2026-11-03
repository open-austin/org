---
attention: live
reviewed: 2026-11-02
---
# Open Austin workflow refresh
Opened 2026-11-02. Stable slug: `org-workflow-refresh`. [Tasks](org-workflow-refresh.todo.md).

## Purpose and scope
Reconcile this repository with the move of general organizational task management to Slack Lists. GitHub still owns repository implementation and retained history; Open Roles and Partner Intake need their actual current ownership checked rather than blanket retirement. This spike owns the refresh investigation and concrete change proposals, not implementation of the underlying organizational tasks.

The user authorized preparing retirement of Org Kanban automation and its Project, deleting the weekly-meeting skill, and closing actual operational task issues after checking their Slack successor-link comments. Engagement intake, contributor records and Open Roles are excluded from blanket cleanup. The local source/policy patch is prepared; publication, Project closure and the exact first issue batch remain subject to the parent’s reviewed-plan rules. Keep private interpretation and raw service records out of this public record. No adaptation branch or policy ID is retired by this patch.

## Baseline and live evidence
Repository main advertised `785910f87c2fa3a2ba9da7d12b4e036b3da69289` on 2026-11-02. The existing Project Workflows adaptation is `57bd7310f8e9b63c2832ae8ea3c4e5df0c1719c2`, branch `project/org`; no package/config/pin changes were made here.

Live read-only GitHub inspection returned 72 open issues and 13 enabled Actions workflows. Org Kanban has 92 items: 30 Done, 48 To Do, 12 In Progress, one On Deck and one Blocked. Open Roles has 22 items: nine Open and thirteen Filled. Both item-list responses report totalCount equal to retrieved count. No retrieved open issue is in its board’s terminal column, and no retrieved closed issue is in a nonterminal column. Open issue #539 is not on either of these two boards. This is a point-in-time consistency check, not evidence that GitHub remains the correct operational task system.

Coverage: all 72 exact issue records and 161 comments were retrieved with complete native-tool comment coverage. Fifty issues have Slack Lists successor links in comments. The first five operational-task threads and exact successor records are verified. Remaining destination eligibility, private shared Docs, native Projects settings and actual scheduled-run outcomes are not fully reconciled. Open-only discovery cannot prove a completed historical migration. No closure eligibility is established yet.

## Every package addition and its owner
Comparison is the actual local patch against shared `79dddf9742c282d184c65d5c5ef87a142900897f`, not a hypothetical extension inventory. The only skill-body additions are these three appended sections.

| Addition | Exact substance | Existing coverage and disposition |
| --- | --- | --- |
| Capture: ownership | Save organization/tooling/process subjects here; another community project owns its own subjects; scope is not infrastructure-only. | This is project scope. Keep the explicit boundary in parent AGENTS when relocating it. Shared Capture already resolves the owning project; no alternate capture algorithm is needed. |
| Capture: old records | Preserve related list entries without duplicates. | Shared Capture’s One visible note per subject already preserves legacy entries in place and forbids incidental bulk migration. Redundant package text can be removed in an approved reconciliation without a replacement file. |
| Capture: authority | Capture/parking creates no GitHub backlog or external-write permission; follow privacy/governance/reviewed plans. | Parent AGENTS Process/Skills and Write Safety already cover this; shared Capture also grants no task/publication authority. No local procedure file is needed. |
| Spike: governance | Read parent authority/write rules; never agent-edit contributor-policy.md. | Parent AGENTS explicitly protects that file. Preserve the parent rule, not a copied shared-skill paragraph. |
| Spike: write checks | Dry runs, reviewed bulk plans, destructive-action limits and notification impact as relevant. | Parent Write Safety already states these obligations; FOLLOW-WORKFLOWS preserves Org QA. A procedural checklist may reference the owners rather than repeat their authority. |
| Spike: substantive QA | API/rate-limit behavior, auth/permission boundaries, recovery; name the expected dry-run or board/issue result. | These are useful checks when code can write to services, not evidence that another procedure artifact is needed. Existing parent write rules and affected-code tests can own them. The retirement patch is checked with offline Roles routing/reopen fixtures; no new skill or workflows folder is introduced. |
| Spike: human QA | Public copy tone, dry-run output and state after an authorized write; identify surface/command and expected result. | Shared Spike already has human-QA machinery. Retain only Org-specific examples in the local review procedure; no change to shared spike lifecycle. |
| Spike: durable evidence | Keep confirmed API behavior with its owning tool/durable docs; update auth examples without secrets. | Tool documentation and parent Auth/Process are the owners. Preserve links and evidence during reconciliation, not another authority layer. |
| Triage: meaningful content | Preserve board/process friction, contributor context, concrete wording, governance and notification concerns. | Shared Triage’s Preservation Rule already preserves concrete examples, uncertainty, references and reasons. Org scope remains valid after general task management moves. No triage algorithm fork is demonstrated. |
| Triage: existing records | Pins/future ideas remain valid; no bulk migration. | Shared Triage/Capture already preserve legacy records and require an actual resumption decision. No replacement file is needed. |
| Triage: service permission | No GitHub comments/edits, board moves, Slack posts or shared-Doc writes through triage. | Parent exact-write and reviewed-plan rules cover these services. Scratch routing grants no service mutation authority. |
| Triage: privacy | Exclude private contributor details, tokens and webhook URLs from public notes. | Parent Auth/Write Safety and shared Capture’s privacy boundary already apply. Keep the parent owner; do not duplicate secret-handling rules in a shared package adaptation. |

Conclusion: Capture and Triage need no unique implementation. Parent scope/write/privacy rules and relevant code checks cover the remainder. No separate service-change QA skill or workflows folder is justified by this evidence. Existing package appendices/branch remain intact; the actual local automation/policy retirement patch is described below.

## Guidance findings at the initial baseline
- README Purpose and AGENTS What This Repo Is still describe GitHub issues/boards as general organization operations. Replace that framing with repository tooling/history and explicitly selected remaining operational systems.
- skills/process-weekly-meeting/SKILL.md routes every credible organizational action through GitHub search/create. It must select the action’s actual current system first; general operational work must not become new GitHub issues just because this old procedure says so. Canonical meeting notes, authorship, no-parallel-minutes and exact-write approval remain useful.
- README Board Automation describes thirteen current implementations as general task machinery. Keep accurate implementation evidence while distinguishing pending retirement of Org Kanban from any retained Roles/Partner processes.
- PRESERVE-SYNC and DESIGN-TRIGGERS were adopted on November 2 and explicitly preserve the existing native-close/polling architecture. Do not silently disable it under a documentation refresh. Prepare exact policy and automation amendments together if its operating purpose ends.
- TODO’s Automation residual QA says the automation is live/working based on older work. Enabled workflow state is verified; actual delivery and current business usefulness are separate checks. Update those claims only with actual run evidence or clearly dated history.

## Automation dependencies before issue cleanup
The six Org Kanban behaviors are add-issue-to-kanban, close-to-done, reopened-to-todo, archive-old-done, blocked-dependency-sync and the Org Kanban half of board-reopen-reconcile. Open-role-add also removes reclassified cards from Org Kanban, so it is a cross-board dependency, not an independent role-only file.

The retained-role question covers open-role-add, label-open-role-from-form, closed-to-filled, open-role-reopened, archive-old-filled, stale-role-warning, role-pipeline-report and the Roles half of board-reopen-reconcile. There are thirteen files in total because the reconciler and routing behavior cross board boundaries. No native Auto-close settings were changed or freshly verified.

Closing a source issue invokes close-to-done or closed-to-filled when applicable. The poller can reopen a closed issue left in a nonterminal column after its ten-minute fresh-close guard. Scheduled archive, blocker sync, stale-role comments and the monthly Slack report also have ongoing effects. Plan retirement in dependency order; do not close a batch and then discover automation is restoring it.

## First issue-routing inventory
These are investigation cohorts, not closure recommendations. Every source-state change needs the full relevant thread, actual current destination/owner, useful history/backlinks and a reviewed exact action. A task being tracked in Slack does not mean the work is completed.

| Issue | Title | First review cohort |
| --- | --- | --- |
| [#389](https://github.com/open-austin/org/issues/389) | foundations and grants fundraising | General operational/planning: reconcile current Slack/Doc owner |
| [#396](https://github.com/open-austin/org/issues/396) | Seek out more free NPO access to software | Idea/reference: preserve context; do not call completed |
| [#405](https://github.com/open-austin/org/issues/405) | Collate all the software we're using | General operational/planning: reconcile current Slack/Doc owner |
| [#417](https://github.com/open-austin/org/issues/417) | recurring supporter swag tiers | General operational/planning: reconcile current Slack/Doc owner |
| [#427](https://github.com/open-austin/org/issues/427) | Reorg github teams | Technical or mixed: confirm actual implementation repository |
| [#435](https://github.com/open-austin/org/issues/435) | Open Role: Community Stakeholder Coordinators (evergreen) | Open Roles: verify retained hiring ownership |
| [#440](https://github.com/open-austin/org/issues/440) | Open Role: Data analysts (evergreen) | Open Roles: verify retained hiring ownership |
| [#461](https://github.com/open-austin/org/issues/461) | Open Role: Social Media Coordinators (evergreen) | Open Roles: verify retained hiring ownership |
| [#462](https://github.com/open-austin/org/issues/462) | Open Role: Technical Writers (on pause) | Open Roles: verify retained hiring ownership |
| [#463](https://github.com/open-austin/org/issues/463) | Switch from Open Collective to new donations and reimbursement platform | General operational/planning: reconcile current Slack/Doc owner |
| [#469](https://github.com/open-austin/org/issues/469) | public policy scraper (mykle tomlinson) | Partner Intake: verify retained process ownership |
| [#471](https://github.com/open-austin/org/issues/471) | Research Hub (childcare) <> WFD CCQI | General operational/planning: reconcile current Slack/Doc owner |
| [#472](https://github.com/open-austin/org/issues/472) | OneBus <> Tisha | General operational/planning: reconcile current Slack/Doc owner |
| [#473](https://github.com/open-austin/org/issues/473) | update request form | General operational/planning: reconcile current Slack/Doc owner |
| [#474](https://github.com/open-austin/org/issues/474) | Research and iterate volunteer onboarding | General operational/planning: reconcile current Slack/Doc owner |
| [#475](https://github.com/open-austin/org/issues/475) | food signals (amanda rochlich) | Partner Intake: verify retained process ownership |
| [#476](https://github.com/open-austin/org/issues/476) | Check whether Open Austin team docs are up to date | General operational/planning: reconcile current Slack/Doc owner |
| [#477](https://github.com/open-austin/org/issues/477) | Utilize Google for Nonprofits ad grant | General operational/planning: reconcile current Slack/Doc owner |
| [#478](https://github.com/open-austin/org/issues/478) | Update stale wiki knowledgebase docs | General operational/planning: reconcile current Slack/Doc owner |
| [#479](https://github.com/open-austin/org/issues/479) | Choose and implement an org credential management solution | General operational/planning: reconcile current Slack/Doc owner |
| [#480](https://github.com/open-austin/org/issues/480) | cap metro/joon/get-there: Onboarding | Partner Intake: verify retained process ownership |
| [#481](https://github.com/open-austin/org/issues/481) | Casa Marianella - Resume Builder | Partner Intake: verify retained process ownership |
| [#482](https://github.com/open-austin/org/issues/482) | QWELL - Queer-friendly resources | Partner Intake: verify retained process ownership |
| [#484](https://github.com/open-austin/org/issues/484) | Infrastructure Roadmap | General operational/planning: reconcile current Slack/Doc owner |
| [#488](https://github.com/open-austin/org/issues/488) | Create a repeatable onboarding and access-provisioning process | General operational/planning: reconcile current Slack/Doc owner |
| [#498](https://github.com/open-austin/org/issues/498) | Security Processes epic: access, permissions, and credentials | General operational/planning: reconcile current Slack/Doc owner |
| [#499](https://github.com/open-austin/org/issues/499) | Automate Google forms for data research hub to github repo | Technical or mixed: confirm actual implementation repository |
| [#500](https://github.com/open-austin/org/issues/500) | CoP meeting ideas, workshops, tutorials, subjects, speakers  | Idea/reference: preserve context; do not call completed |
| [#501](https://github.com/open-austin/org/issues/501) | Move bank access etc over to Rachel as new Finance Chair | General operational/planning: reconcile current Slack/Doc owner |
| [#502](https://github.com/open-austin/org/issues/502) | Tutorialize new Finance Chair on Zoha books | General operational/planning: reconcile current Slack/Doc owner |
| [#503](https://github.com/open-austin/org/issues/503) | Tutorialize new Communications chair on how to use Buffer and other social media accounts | General operational/planning: reconcile current Slack/Doc owner |
| [#504](https://github.com/open-austin/org/issues/504) | Implement public Slack join link with anti-spam protections | Technical or mixed: confirm actual implementation repository |
| [#505](https://github.com/open-austin/org/issues/505) | Runtime Systems epic: hosting, DNS, and deployment | General operational/planning: reconcile current Slack/Doc owner |
| [#506](https://github.com/open-austin/org/issues/506) | Design and build volunteer management system (VRM) | Technical or mixed: confirm actual implementation repository |
| [#507](https://github.com/open-austin/org/issues/507) | Open Role: UX/Web Designer (OneBus) | Open Roles: verify retained hiring ownership |
| [#508](https://github.com/open-austin/org/issues/508) | Transfer ownership of Landlord Mapper domain to Infrastructure | Technical or mixed: confirm actual implementation repository |
| [#509](https://github.com/open-austin/org/issues/509) | Establish org wide DNS policy | General operational/planning: reconcile current Slack/Doc owner |
| [#510](https://github.com/open-austin/org/issues/510) | Establish org wide hosting policy | General operational/planning: reconcile current Slack/Doc owner |
| [#511](https://github.com/open-austin/org/issues/511) | Unstick the backend issues with Landlord Mapper | Technical or mixed: confirm actual implementation repository |
| [#512](https://github.com/open-austin/org/issues/512) | Document new Team org structure in the Wiki | General operational/planning: reconcile current Slack/Doc owner |
| [#516](https://github.com/open-austin/org/issues/516) | Open Role: Community Engagement Ambassador (multiple, evergreen) | Open Roles: verify retained hiring ownership |
| [#517](https://github.com/open-austin/org/issues/517) | Test and iterate the Partner Intake process | Partner Intake: verify retained process ownership |
| [#518](https://github.com/open-austin/org/issues/518) | Define and pilot a stakeholder-liaison model for Product Teams and CoPs | General operational/planning: reconcile current Slack/Doc owner |
| [#520](https://github.com/open-austin/org/issues/520) | Define and pilot a volunteer-stewardship process | General operational/planning: reconcile current Slack/Doc owner |
| [#521](https://github.com/open-austin/org/issues/521) | Build a repeatable volunteer-recognition process | General operational/planning: reconcile current Slack/Doc owner |
| [#523](https://github.com/open-austin/org/issues/523) | People Systems epic: VRM and people/org records | General operational/planning: reconcile current Slack/Doc owner |
| [#524](https://github.com/open-austin/org/issues/524) | Define the org access and permissions matrix | General operational/planning: reconcile current Slack/Doc owner |
| [#526](https://github.com/open-austin/org/issues/526) | Figure out more permanent long term venue solution for CoPs | General operational/planning: reconcile current Slack/Doc owner |
| [#529](https://github.com/open-austin/org/issues/529) | Re-engage former Open Austinites | Idea/reference: preserve context; do not call completed |
| [#530](https://github.com/open-austin/org/issues/530) | Refresh website content in accordance with strategy considerations | General operational/planning: reconcile current Slack/Doc owner |
| [#531](https://github.com/open-austin/org/issues/531) | Draft an Open Austin privacy policy | General operational/planning: reconcile current Slack/Doc owner |
| [#532](https://github.com/open-austin/org/issues/532) | Receive and continue Ryan Klemz's Education / onboarding handoff | General operational/planning: reconcile current Slack/Doc owner |
| [#534](https://github.com/open-austin/org/issues/534) | Tabling: Austin Women in Technology Community Happy Hour (September) | General operational/planning: reconcile current Slack/Doc owner |
| [#535](https://github.com/open-austin/org/issues/535) | Explore insurance options | General operational/planning: reconcile current Slack/Doc owner |
| [#536](https://github.com/open-austin/org/issues/536) | Public no-login intake + update form for the VRM (Fillout) | Technical or mixed: confirm actual implementation repository |
| [#537](https://github.com/open-austin/org/issues/537) | Retire the GitHub contributor profiles (cut over to the VRM) | Technical or mixed: confirm actual implementation repository |
| [#538](https://github.com/open-austin/org/issues/538) | Operationalize VRM for new contributor onboarding | General operational/planning: reconcile current Slack/Doc owner |
| [#539](https://github.com/open-austin/org/issues/539) | Sources of volunteer recruitment | Idea/reference: preserve context; do not call completed |
| [#541](https://github.com/open-austin/org/issues/541) | Project Team Survey - Infrastructure | General operational/planning: reconcile current Slack/Doc owner |
| [#542](https://github.com/open-austin/org/issues/542) | Claim and maintain the Candid/GuideStar profile | General operational/planning: reconcile current Slack/Doc owner |
| [#543](https://github.com/open-austin/org/issues/543) | Establish annual conflict-of-interest disclosure for board and staff | General operational/planning: reconcile current Slack/Doc owner |
| [#544](https://github.com/open-austin/org/issues/544) | Publish financial information on open-austin.org | General operational/planning: reconcile current Slack/Doc owner |
| [#545](https://github.com/open-austin/org/issues/545) | Engage the approved registered agent service and file the change with the state | General operational/planning: reconcile current Slack/Doc owner |
| [#546](https://github.com/open-austin/org/issues/546) | Take down old github.io website  | Technical or mixed: confirm actual implementation repository |
| [#550](https://github.com/open-austin/org/issues/550) | Data Research Hub Request Intake - "I agree!" | General operational/planning: reconcile current Slack/Doc owner |
| [#551](https://github.com/open-austin/org/issues/551) | Open Role: Onboarding Coordinator (multiple, evergreen) | Open Roles: verify retained hiring ownership |
| [#552](https://github.com/open-austin/org/issues/552) | Open Role: Community Relations Team (multiple, evergreen) | Open Roles: verify retained hiring ownership |
| [#553](https://github.com/open-austin/org/issues/553) | Open Role: Recognition Coordinator (multiple, evergreen) | Open Roles: verify retained hiring ownership |
| [#554](https://github.com/open-austin/org/issues/554) | Design the durable project-idea intake (oa-labs-requests) | Technical or mixed: confirm actual implementation repository |
| [#555](https://github.com/open-austin/org/issues/555) | Partner intake: technical form/tool implementation (provisional) | Technical or mixed: confirm actual implementation repository |
| [#556](https://github.com/open-austin/org/issues/556) | List of fellow non-profit and activist orgs we can potentially partner with and recruit from | Idea/reference: preserve context; do not call completed |
| [#557](https://github.com/open-austin/org/issues/557) | Grant Rachel Live Oak access | General operational/planning: reconcile current Slack/Doc owner |

## Deliverable sequence
First finish owner/thread/destination evidence and the exact guidance amendments. Then present small approval slates for (a) local guidance/policy/procedure changes, (b) the exact automation/native-settings retirement or retention, and (c) small source-issue cohorts with explicit state/reason/backlinks. Re-fetch before authorized mutations and verify actual final state. Do not bulk close all 72 issues or infer approval from this inventory.

## Prepared retirement patch — November 2
Delete the five Kanban-only files: add-issue-to-kanban.yaml, close-to-done.yaml, reopened-to-todo.yaml, archive-old-done.yaml and blocked-dependency-sync.yaml. Remove Kanban cleanup from open-role-add and the Kanban call from board-reopen-reconcile, retaining Roles add/status behavior, five-minute polling, dry_run and the 600-second fresh-close guard. Eight role-related workflows remain. Delete skills/process-weekly-meeting/SKILL.md and its live routing/configuration examples. Update README/AGENTS/CONTRIBUTING and the two affected synchronization policies for the actual narrowed scope; preserve contributor-policy.md byte-for-byte.

The local patch is not deployed. Hosted Actions remain at the previous source until approved publication. Before closing the Project, publish and verify the narrowed workflow tree, inspect any in-flight former Kanban jobs and handle only explicitly selected remaining runs. Close Org Kanban Project #9, retaining its contents/history; do not delete it or alter Roles/Engagement projects. Agent Hands currently has no Project-close operation, so the exact gh project close command is the supported fallback under explicit approval. Do not infer that closing a Project alone disables every external workflow.

Eight YAML files parse and every inline shell passes bash -n. Offline fixtures exercise role routing with only Roles API calls, dry-run zero writes, and the Roles-only reopener’s terminal/fresh-close guards. The policy graph/index check passes and index regeneration is a no-op. These checks do not establish hosted deployment, native settings or actual scheduled delivery.

## First closure batch — prepared, not executed
Five operational task issues have complete retrieved comment histories, explicit successor comments and verified current successor records: #501, #502, #535, #542 and #557. The exact first batch is presented in chat; each source goes from open to closed with reason not_planned because GitHub tracking ends while work continues in Slack. No new comment, label, assignee or Slack mutation is included. Closures may notify subscribers. Native previews report zero writes. Keep private destination contents and preview/recovery material out of this public repo.

Remaining review cohorts include 22 issues without a Slack Lists comment and the protected intake/profile/role cases, including any such case among the fifty linked records. A successor URL alone does not authorize closing an excluded intake/profile/role record. The four roadmap/epic issues without a Lists comment need their actual roadmap-document successors established before any source-state proposal.

Pre-deployment readback on November 2 identifies Org Kanban as Project #9, ID PVT_kwDOAA7NZM4AqQF8, currently open. At that read there were no in-progress or queued Org Actions runs. Recheck before execution; this snapshot is not a lock.

## Execution authorization — November 2
Aslan approved the exact first batch: close issues #501, #502, #535, #542 and #557 with reason not_planned after rechecking successor comments, and publish the prepared Org retirement patch, disable the five retired workflows and close Project #9 while retaining its contents. No new comments or changes to Roles/intake/contributor records are included. Shared workflow-source publication remains outside this authorization.
