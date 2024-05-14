import mido

# Fonction à appeler pour convertir un fichier midi
def convertMidi(
        midiFile, 
        MinTimeOffPedal=0.2, 
        MinTimeOffNote=0.1, 
        MinTimeOnNote=0.05, 
        MaxTimeOnNote=4,
        ls_deleteTracks=[],
        MesurePedal=0
        ):

    # Lit le fichier midi et on extrait ses données
    try:
        midiMusic = mido.MidiFile(midiFile)
    except:
        print('[ERROR] File not found.')
        return False

    # Supprime les pistes désignées
    if not ls_deleteTracks == []:
        i = 0
        for isDelete in ls_deleteTracks:
            if isDelete:
                del midiMusic.tracks[i]
            else:
                i += 1

    # Creation d'une liste pour enregistrer les messages (note 20 indique la pédale)
    ls_noteInfo = []

    # Lancement de la musique et enregistre chaque message à quel temps il est arrivé avec aussi la pédal

    # la fonction "playNoTime()"" et une fonction qu'on a rajouté directement dans la librairie Mido à côté de "play"
    # Si vous utilisez visual studio code vous pouvez faire un clic droit sur la fonction play de mido puis "Go to Definition" et ensuite copiez collez ce code à cette endroit:
    # Nom du fichier : midifiles.py
    """
        def playNoTime(self):

            for msg in self:
                if isinstance(msg, MetaMessage):
                    continue
                else:
                    yield msg
    """

    CurrentTime = 0
    for message in midiMusic.playNoTime():

        # Calcul du temps du message
        CurrentTime += message.time

        match message.type:

            case 'note_on':
                if message.velocity == 0:
                    # C'est un message de désactivation de note
                    ls_noteInfo.append([CurrentTime, False, message.note])
                else:
                    # C'est un message d'activation de note
                    ls_noteInfo.append([CurrentTime, True, message.note])

            case 'note_off':
                # C'est un message de désactivation de note
                ls_noteInfo.append([CurrentTime, False, message.note])

            case 'control_change':
                if message.control == 64:
                    if message.value == 0:
                        # C'est un message de désactivation de pédale
                        ls_noteInfo.append([CurrentTime, False, 20])
                    else:
                        # C'est un message d'activation de pédale
                        ls_noteInfo.append([CurrentTime, True, 20])

    # Analyse des temps dans le ficher Midi et modification des ses temps
    delta = 0
    for cursor in range(len(ls_noteInfo)):

        # Si c'est un message de désactivation
        if ls_noteInfo[cursor][1] == False:
            # Si c'est un message de pédale
            if ls_noteInfo[cursor][2] == 20:
                modifTimeMsg(ls_noteInfo, cursor, False, False, MinTimeOffPedal)
            else:
                if not modifTimeMsg(ls_noteInfo, cursor, False, False, MinTimeOffNote):
                    modifTimeMsg(ls_noteInfo, cursor, True, False, MinTimeOnNote)
                modifTimeMsg(ls_noteInfo, cursor, True, True, MaxTimeOnNote)
            ls_noteInfo.sort(key=lambda x: x[0])

    # Réorgination de la liste suivant les temps
    ls_noteInfo.sort(key=lambda x: x[0])

    # Va chercher le tempo dans la musique midi
    isFind = False
    for track in midiMusic.tracks:
        if isFind:
            break
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                isFind = True
                break

    # Va chercher le message de la time signature dans la musique midi
    isFind = False
    for track in midiMusic.tracks:
        if isFind:
            break
        for msg in track:
            if msg.type == 'time_signature':
                MessageTimeSignature = msg
                isFind = True
                break

    # Arondit les temps à la milli seconde
    for noteInfo in ls_noteInfo:
        noteInfo[0] = round(noteInfo[0], 3)

    # set le tick per beat
    ticksPerBeat = 360

    # Réecrit la mémoire ls_noteInfo en un fichier midi

    # Créer une nouvelle piste avec des messages
    track = mido.MidiTrack()

    # Ajouter le message du time signature
    track.append(MessageTimeSignature)

    # Ajouter le message du tempo
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Ajouter le message qui indique que c'est un piano
    track.append(mido.Message('program_change', program=0))

    # Ajoute les notes dans la track
    for cursor in range(len(ls_noteInfo)):

        # Calcul du temp dans le message
        if cursor == 0:
            deltaTime = 0
        else:
            deltaTime = mido.second2tick(ls_noteInfo[cursor][0] - ls_noteInfo[cursor - 1][0], ticksPerBeat, tempo)

        if ls_noteInfo[cursor][2] == 20:
            if ls_noteInfo[cursor][1]:
                # C'est un message d'activation de pédal
                track.append(mido.Message('control_change', control=64,  value=100, time=deltaTime))
            else:
                # C'est un message de désactivation de pédal
                track.append(mido.Message('control_change', control=64,  value=0, time=deltaTime))
        else:
            if ls_noteInfo[cursor][1]:
                # C'est un message d'activation de note
                track.append(mido.Message('note_on', note=ls_noteInfo[cursor][2],  velocity=100, time=deltaTime))
            else:
                # C'est un message de désactivation de note
                track.append(mido.Message('note_off', note=ls_noteInfo[cursor][2],  velocity=0, time=deltaTime))

    # Ajoute à la fin le message de fin de piste
    track.append(mido.MetaMessage('end_of_track', time=0))

    # Créer un objet MidiFile et ajouter la piste
    midiFileOut = mido.MidiFile() 

    # Set le ticksPerBeat 
    midiFileOut.ticks_per_beat = ticksPerBeat

    # Ajoute la track au fichier midi
    midiFileOut.tracks.append(track)

    # Enregistrer le fichier MIDI
    midiFileOut.save(midiFile[:midiFile.rfind('.')] + '_Conv.mid')

    print('[INFO] The file <', midiFile[:midiFile.rfind('.')] + '_Conv.mid > was create.',)

    return True
    
# Fonction pour aller chercher le message d'activation, caluler la différence de temps et modifier sa postion dans le temps s'il ne respecte pas le temps maximal ou minimal
def modifTimeMsg(ls_noteInfo, cursor, off_on, Min_max, time):

    delta = 0
    while True:
        # S'il est arrivé a la fin du fichier alors il passe au prochain
        if cursor + delta >= len(ls_noteInfo) or cursor + delta < 0:
            return False
        
        # A trouvé le message
        if ls_noteInfo[cursor + delta][1] and ls_noteInfo[cursor + delta][2] == ls_noteInfo[cursor][2]:
            # Modification de la position dans le temps du message de désactivation suivant la modification de temps
            # calcul de la difference de temps entre les deux messages
            deltaTime = abs(ls_noteInfo[cursor][0] - ls_noteInfo[cursor + delta][0])
            if off_on:
                if Min_max:
                    # Si le temps maximal activé n'est pas assez grand on le raccourcit
                    if deltaTime > time:
                        ls_noteInfo[cursor][0] -= deltaTime - time
                        #print("Modif max time on Message", cursor + 1)
                        return True
                else:
                    # Si le temps miminal activé n'est pas assez grand on l'allonge
                    if deltaTime < time:
                        ls_noteInfo[cursor][0] += time - deltaTime
                        #print("Modif min time on Message", cursor + 1)
                        return True
            else:
                if Min_max:
                    # Si le temps maximal désactivé n'est pas assez grand on le raccourcit
                    if deltaTime > time:
                        ls_noteInfo[cursor][0] += deltaTime - time
                        #print("Modif max time off Message", cursor + 1)
                        return True
                else:
                    # Si le temps minimal désactivé n'est pas assez grand on l'allonge
                    if deltaTime < time:
                        ls_noteInfo[cursor][0] -= time - deltaTime
                        #print("Modif min time off Message", cursor + 1)
                        return True
            return False 
        else:
            if off_on:
                # Si ce n'est pas le précédent message regarde encore plus en arrière
                delta -= 1
            else:
                # Si ce n'est pas le prochain message regarde encore plus en avant
                delta += 1