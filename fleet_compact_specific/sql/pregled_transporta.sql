-- drop view fleet_pregled_transporta
create or replace view fleet_pregled_transporta as
select 	
	tbl.vozilo,
	tbl.vozac,
	tbl.relacija,
	tbl.datum,
	tbl.relacija::text || ' (' || to_char(tbl.datum, 'dd.MM.yyyy') || ')' as relacija_datum,
	tbl.prevezeno_tona, 
	tbl.vrijednost_km, 
	tbl.gorivo_litara, 
	tbl.gorivo_vrijednost, 
	(0.1453*tbl.gorivo_vrijednost) as gorivo_pdv,
	(0.8547*tbl.gorivo_vrijednost) as gorivo_bez_pdv,
	tbl.troskovi_akontacije,
	tbl.troskovi_putarine,
	(0.1*vrijednost_km) as zarada_vozaca,
	tbl.troskovi_pranje_cisterne,
	( 0.9*vrijednost_km - (tbl.troskovi_putarine+tbl.troskovi_akontacije+tbl.troskovi_pranje_cisterne+0.8547*tbl.gorivo_vrijednost) ) as ruc,
	tbl.predjeno_km,
	((tbl.gorivo_litara/tbl.predjeno_km)*100) as potrosnja_na_100_km
	
	
from
(
	select
	
	tro.distance as relacija
	,veh.license_plate as vozilo
	,res.name as vozac
	,tro.date as datum
	,(
		select coalesce(sum(fak.prevezeno_tona), 0)
		from fleet_invoice fak
		where fak.travel_order_id = tro.id
	) as prevezeno_tona
	,(
		select coalesce(sum(fak.ukupan_iznos), 0)
		from fleet_invoice fak
		where fak.travel_order_id = tro.id
		
	) as vrijednost_km
	,(
		select coalesce(sum(fuel.liter), 0)
		from fleet_vehicle_log_fuel fuel
		left join fleet_vehicle_cost cst on (cst.id = fuel.cost_id)
		where cst.travel_order_id = tro.id
	) as gorivo_litara
	,(
		select coalesce(sum(cst.amount), 0)
		from fleet_vehicle_cost cst
		where cst.travel_order_id = tro.id and cst.cost_type = 'fuel'
	) as gorivo_vrijednost
	,(
		select coalesce(sum(cst.amount), 0)
		from fleet_vehicle_cost cst
		left join fleet_service_type type on (type.id = cst.cost_subtype_id)
		where cst.travel_order_id = tro.id and type.name like 'Putni troškovi'
	) as troskovi_akontacije
	,(
		select coalesce(sum(cst.amount), 0)
		from fleet_vehicle_cost cst
		left join fleet_service_type type on (type.id = cst.cost_subtype_id)
		where cst.travel_order_id = tro.id and type.name like 'Putarina'
	) as troskovi_putarine
	,(
		select coalesce(sum(cst.amount), 0)
		from fleet_vehicle_cost cst
		left join fleet_service_type type on (type.id = cst.cost_subtype_id)
		where cst.travel_order_id = tro.id and type.name like 'Pranje%'
	) as troskovi_pranje_cisterne
	, tro.total_km as predjeno_km

	from fleet_vehicle_travel_order tro
	left join fleet_vehicle veh on (veh.id = tro.vehicle_id)
	left join hr_employee emp on (emp.id = tro.driver1_id)
	left join resource_resource res on (res.id = emp.resource_id)
) as tbl
