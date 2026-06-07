%% Base de conocimiento para el sistema experto de recomendación de motocicletas para consesionaria.
% Base de hechos
% moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio)

:- dynamic moto/6.

moto(honda, cb150, urbana, 150, 38000, 2023).
moto(honda, dio110, scooter, 110, 32000, 2023).
moto(honda, crf250, todoterreno, 250, 75000, 2023).
moto(honda, cb300f, naked, 293, 85000, 2024).
moto(honda, xr190l, todoterreno, 184, 65000, 2024).
moto(yamaha, mt03, naked, 321, 95000, 2023).
moto(yamaha, wr250, todoterreno, 250, 78000, 2022).
moto(yamaha, tmax560, scooter, 560, 140000, 2023).
moto(yamaha, fz25, naked, 249, 89000, 2024).
moto(yamaha, r3, deportiva, 321, 125000, 2024).
moto(kawasaki, ninja650, deportiva, 650, 145000, 2023).
moto(kawasaki, z400, naked, 399, 98000, 2022).
moto(kawasaki, versys300, touring, 296, 88000, 2023).
moto(kawasaki, ninja400, deportiva, 399, 155000, 2024).
moto(kawasaki, klx300, todoterreno, 292, 118000, 2024).
moto(suzuki, gixxer150, deportiva, 155, 42000, 2023).
moto(suzuki, vstrom650, touring, 645, 155000, 2023).
moto(suzuki, gn125, urbana, 125, 30000, 2022).
moto(suzuki, gixxer250, deportiva, 249, 95000, 2024).
moto(suzuki, burgman125, scooter, 124, 58000, 2024).
moto(bmw, r1250gs, touring, 1254, 320000, 2023).
moto(bmw, g310r, naked, 313, 110000, 2023).
moto(bmw, f750gs, touring, 853, 290000, 2024).
moto(bmw, g310gs, touring, 313, 135000, 2024).
moto(bajaj, dominar400, naked, 373, 92000, 2023).
moto(bajaj, pulsarns200, deportiva, 199, 55000, 2023).
moto(bajaj, avenger220, touring, 220, 68000, 2024).
moto(bajaj, pulsarns160, deportiva, 160, 48000, 2024).
moto(ktm, duke390, naked, 373, 115000, 2023).
moto(ktm, exc300, todoterreno, 293, 135000, 2023).
moto(ktm, rc390, deportiva, 373, 140000, 2024).
moto(ktm, adventure390, touring, 373, 150000, 2024).
moto(italika, ft150, urbana, 150, 22000, 2023).
moto(italika, ws175, todoterreno, 175, 28000, 2023).
moto(italika, dm250, touring, 250, 48000, 2024).
moto(italika, rt250, deportiva, 250, 52000, 2024).
moto(vento, rocketman250, urbana, 250, 45000, 2024).
moto(vento, nitrox200, deportiva, 200, 42000, 2024).
moto(benelli, tnt300, naked, 300, 105000, 2024).
moto(benelli, trk251, touring, 249, 118000, 2024).
moto(cfmoto, nk300, naked, 292, 92000, 2024).
moto(cfmoto, mt450, touring, 449, 175000, 2024).
moto(harley, street750, touring, 749, 180000, 2023).
moto(ducati, monster937, naked, 937, 320000, 2024).
moto(ducati, supersport950, deportiva, 937, 380000, 2024).
moto(triumph, speed400, naked, 398, 115000, 2024).
moto(triumph, tiger660, touring, 660, 220000, 2024).

moto(royalenfield, hunter350, urbana, 349, 95000, 2024).
moto(royalenfield, himalayan450, touring, 452, 185000, 2024).

usoEstilo(ciudad, urbana).
usoEstilo(ciudad, scooter).
usoEstilo(trabajo, urbana).
usoEstilo(trabajo, scooter).
usoEstilo(carretera, touring).
usoEstilo(carretera, naked).
usoEstilo(terraceria, todoterreno).
usoEstilo(deportivo, deportiva).
usoEstilo(deportivo, naked).

experienciaCilindrada(principiante, 0, 200).
experienciaCilindrada(intermedio, 150, 400).
experienciaCilindrada(avanzado, 300, 1300).

recomendarMotoDatos(Uso, PresupuestoMax, Experiencia, Marca, Modelo, Estilo, Cilindrada, Precio, Anio) :-
    usoEstilo(Uso, Estilo),
    experienciaCilindrada(Experiencia, MinCil, MaxCil),
    moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio),
    Precio =< PresupuestoMax,
    Cilindrada >= MinCil,
    Cilindrada =< MaxCil.

buscarPorEstilo(Estilo) :-
    moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio),
    write(Marca), write(' '), write(Modelo),
    write(' | '), write(Cilindrada), write('cc'),
    write(' | $'), write(Precio),
    write(' | '), write(Anio),
    nl,
    fail.
buscarPorEstilo(_).



buscarPorPrecio(Min, Max) :-
    moto(Marca, Modelo, Estilo, _, Precio, Anio),
    Precio >= Min,
    Precio =< Max,
    write(Marca), write(' '), write(Modelo),
    write(' | '), write(Estilo),
    write(' | $'), write(Precio),
    write(' | '), write(Anio),
    nl,
    fail.
buscarPorPrecio(_, _).




buscarPorMarca(Marca) :-
    moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio),
    write(Modelo), write(' | '), write(Estilo),
    write(' | '), write(Cilindrada), write('cc'),
    write(' | $'), write(Precio),
    write(' | '), write(Anio),
    nl,
    fail.
buscarPorMarca(_).



buscarPorCilindrada(Min, Max) :-
    moto(Marca, Modelo, Estilo, Cilindrada, Precio, _),
    Cilindrada >= Min,
    Cilindrada =< Max,
    write(Marca), write(' '), write(Modelo),
    write(' | '), write(Estilo),
    write(' | '), write(Cilindrada), write('cc'),
    write(' | $'), write(Precio),
    nl,
    fail.
buscarPorCilindrada(_, _).




buscarPorModelo(Modelo) :-
    moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio),
    write(Marca), write(' '), write(Modelo),
    write(' | '), write(Estilo),
    write(' | '), write(Cilindrada), write('cc'),
    write(' | $'), write(Precio),
    write(' | '), write(Anio),
    nl,
    fail.
buscarPorModelo(_).



buscarPorAnio(Anio) :-
    moto(Marca, Modelo, Estilo, _, Precio, Anio),
    write(Marca), write(' '), write(Modelo),
    write(' | '), write(Estilo),
    write(' | $'), write(Precio),
    nl,
    fail.
buscarPorAnio(_).


gestionarMoto(agregar, Marca, Modelo, Estilo, Cilindrada, Precio, Anio) :-
    assertz(moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio)),
    write('Moto agregada: '),
    write(Marca), write(' '), write(Modelo), nl.

gestionarMoto(eliminar, Marca, Modelo, _Estilo, _Cilindrada, _Precio, _Anio) :-
    retract(moto(Marca, Modelo, _, _, _, _)),
    write('Moto eliminada: '),
    write(Marca), write(' '), write(Modelo), nl.

gestionarMoto(actualizar, Marca, Modelo, NuevoEstilo, NuevaCilindrada, NuevoPrecio, NuevoAnio) :-
    retract(moto(Marca, Modelo, _, _, _, _)),
    assertz(moto(Marca, Modelo, NuevoEstilo, NuevaCilindrada, NuevoPrecio, NuevoAnio)),
    write('Moto actualizada: '),
    write(Marca), write(' '), write(Modelo), nl.