select 
  s1.child_id as first_level_controls
from assessments as a1
inner join relationships as r1 
  on  r1.source_type = "Assessment" 
  and r1.source_id = a1.id
  and r1.destination_type = "Snapshot"
inner join snapshots as s1
  on  s1.id = r1.destination_id
  and s1.child_type = "Control"
where 
      a1.id = 698
;

select 
  s1.child_id as first_level_controls
from assessments as a1
inner join relationships as r1 
  on  r1.destination_type = "Assessment" 
  and r1.destination_id = a1.id
  and r1.source_type = "Snapshot"
inner join snapshots as s1
  on  s1.id = r1.source_id
  and s1.child_type = "Control"
where 
      a1.id = 698

;

select 
  r2.destination_id as second_level_control_dst
from assessments as a1
inner join relationships as r1 
  on  r1.source_type = "Assessment" 
  and r1.source_id = a1.id
  and r1.destination_type = "Snapshot"
inner join snapshots as s1
  on  s1.id = r1.destination_id
  and s1.child_type = "Control"
inner join relationships as r2
  on  r2.source_type = "Control"
  and r2.source_id = s1.child_id
  and r2.destination_type = "Control"
where 
      a1.id = 698

;

select 
  r2.source_id as second_level_control_dst
from assessments as a1
inner join relationships as r1 
  on  r1.source_type = "Assessment" 
  and r1.source_id = a1.id
  and r1.destination_type = "Snapshot"
inner join snapshots as s1
  on  s1.id = r1.destination_id
  and s1.child_type = "Control"
inner join relationships as r2
  on  r2.destination_type = "Control"
  and r2.destination_id = s1.child_id
  and r2.source_type = "Control"
where 
      a1.id = 698

;

select * from assessments where id in (
1

);
