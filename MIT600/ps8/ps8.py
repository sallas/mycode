# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab

#
# PROBLEM 1
#

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        # TODO
        return random.random() < self.clearProb

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO

        if random.random() < (self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        raise NoChildException
            



class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxpop = maxPop
        # TODO


    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO        
        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        # TODO
        temp_list = list()
        for virus in self.viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
        popDensity = self.getTotalPop() / float(self.maxpop)
        for virus in self.viruses:
            try:
                temp = virus.reproduce(popDensity)
            except NoChildException:
                pass
            else:
                temp_list.append(temp)
        self.viruses = self.viruses + temp_list
        return self.getTotalPop()
            
            

#
# PROBLEM 2
#
def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """

    # TODO
    d = 0
    while d < 1:
        pop_list = list()
        virus_list = list()
        for i in range(0,100):
            virus_list.append(SimpleVirus(0.01+d,0.))
        patient = SimplePatient(virus_list,1000)
        pop_list.append(100)
        plot_list = range(0,301)
        for i in range(0,300):
            pop_list.append(patient.update())
        pylab.plot(plot_list,pop_list)
        d += 0.1
    pylab.title('300 hours, Simple Virus, Standard Patient')
    pylab.xlabel('Hours')
    pylab.ylabel('Total amount of viruses')
    pylab.show()
    

class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """


        # TODO
        self.maxbirthprob = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutprob = mutProb


    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        # TODO
        return self.resistances[drug]

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO
        offspring_dict = dict()
        for drug in activeDrugs:
            if self.resistances[drug] == False:
                raise NoChildException
        if random.random() < (self.maxbirthprob * (1 - popDensity)):
            offspring_dict = self.resistances.copy()
            for drug in self.resistances:
                if self.resistances[drug] == True:
                    if random.random() < self.mutprob:
                        offspring_dict[drug] = False
                else:
                    if random.random() < self.mutprob:
                        offspring_dict[drug] = True
            return ResistantVirus(self.maxbirthprob, self.clearProb, offspring_dict, self.mutprob)
        raise NoChildException
            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop
        self.activedrugs = list()

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.activedrugs:
            self.activedrugs.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.activedrugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        numPop = 0
        for virus in self.viruses:
            resistant = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistant = False
                    break
            if resistant:
                numPop += 1
        return numPop


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        temp_list = list()
        for virus in self.viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
        popDensity = self.getTotalPop() / float(self.maxPop)
        for virus in self.viruses:
            try:
                temp = virus.reproduce(popDensity, self.activedrugs)
            except NoChildException:
                pass
            else:
                temp_list.append(temp)
        self.viruses = self.viruses + temp_list
        return self.getTotalPop()


#
# PROBLEM 2
#

def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    for d in range(0,10):
        pop_list = list()
        resist_pop = list()
        virus_list = list()
        for i in xrange(0,100):
            virus_list.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))
        patient = Patient(virus_list,1000)
        pop_list.append(100)
        #plot_list = range(0,301)
        for i in range(0,150):
            pop_list.append(patient.update())
            resist_pop.append(patient.getResistPop(['guttagonol']))
        patient.addPrescription('guttagonol')
        for i in range(0,150):
            pop_list.append(patient.update())
            resist_pop.append(patient.getResistPop(['guttagonol']))
        if d == 0:
            total_pop_list = pylab.array(pop_list[:])
            total_resist_pop = pylab.array(resist_pop[:])
        else:
            total_pop_list += pylab.array(pop_list[:])
            total_resist_pop += pylab.array(resist_pop[:])
    total_resist_pop /= 10.0
    total_pop_list /= 10.0
    pylab.plot(total_pop_list, label = 'Population')
    pylab.plot(total_resist_pop, label = 'resistant population')
    pylab.title('300 hours, Resistant Virus, Patient')
    pylab.xlabel('Hours')
    pylab.ylabel('Virus population/Resistant Population')
    pylab.legend(loc = "best")
    pylab.show()


#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # TODO
    for d in xrange(0,300):
        pop_list = list()
        virus_list = list()
        for i in xrange(0,100):
            virus_list.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))
        patient = Patient(virus_list,1000)
        for i in xrange(0,150):
            patient.update()
        patient.addPrescription('guttagonol')
        for i in xrange(0,150):
            patient.update()
        pop_list.append(patient.getTotalPop())
        if d == 0:
            total_pop_list = pop_list[:]
        else:
            total_pop_list.append(pop_list[0])
    print total_pop_list
    #pylab.plot(total_pop_list, label = 'Population')
    pylab.hist(total_pop_list, bins = 12, range=(0, 600))
    #pylab.plot(total_resist_pop, label = 'resistant population')
    pylab.title('300 hours, Resistant Virus, Patient, Histo')
    pylab.xlabel('Virus population')
    pylab.ylabel('Patients')
    pylab.legend(loc = "best")
    pylab.show()
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO



