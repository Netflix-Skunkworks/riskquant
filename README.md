# riskquant

A library to assist in quantifying risk. To use riskquant:

```bash
python3 setup.py
```

## Using riskquant as a library

### simpleloss  

The simpleloss class uses a single value for frequency, and two values for a magnitude range that are mapped to a [lognormal distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html).  


The inputs to simpleloss are as follows:  

 * Identifier: An identifying label, which need not be unique, (see "Uniqueness of identifiers" below) but is 
  intended to provide a way of identifying the scenario. 
 * Name: The name of the scenario, which should be more descriptive than the identifier.
 * Frequency: The number of times that the loss will occur over some interval of time (e.g. 0.1 means 1 occurrence per 10 years on average).
 * Low loss magnitude: A dollar value of the best-case scenario, given that the loss did occur. All our detection systems worked, so we
  found out about the event and remediated quickly.
 * High loss magnitude: A dollar value of the worst-cases scenario. Our detection systems didn't work, and the problem persisted for a long
  time until it was unavoidable to notice it and stop it.

```python
>> from riskquant import simpleloss
>> s = simpleloss.SimpleLoss("T_PLANKTON", "Plankton steals the Krabby Patty recipe", 0.10, 100000, 1000000)
>> s.annualized_loss()

40400.128269457266
```

### pertloss

The pertloss class uses two values for a magnitude range that are mapped to a lognormal distribution, and
four values for frequency that are used to create a [Modified PERT distribution](https://www.tensorflow.org/probability/api_docs/python/tfp/experimental/substrates/numpy/distributions/PERT).  


The inputs to pertloss are as follows:  

 * Low loss magnitude: A dollar value of the best-case scenario, given that the loss did occur. All our detection systems worked, so we
  found out about the event and remediated quickly.
 * High loss magnitude: A dollar value of the worst-cases scenario. Our detection systems didn't work, and the problem persisted for a long
  time until it was unavoidable to notice it and stop it.
 * Minimum frequency: The lowest number of times a loss will occur over some interval of time
 * Maximum frequency: The highest number of times a loss will occur over some interval of time
 * Most likely frequency: The most likely number of times a loss will occur over some interval of time.  Sets the skew of the distribution.
 * Kurtosis: A number that controls the shape of the PERT distribution, with a default of 4.  Higher values will cause a sharper peak.  
 In FAIR, this is called the "belief in the most likely" frequency, based on the confidence of the estimator in the most likely frequency.  
 With higher kurtosis, more samples in the simulation will be closer to the most likely frequency. 

```python
>> from riskquant import pertloss
>> p = pertloss.PERTLoss(10, 100, .1, .7, .3, kurtosis=1) 
>> simulate_100 = p.simulate_years(100)
>> p.summarize_loss(simulate_100)

{'minimum': 0,
 'tenth_percentile': 0,
 'mode': 0,
 'median': 1,
 'ninetieth_percentile': 2,
 'maximum': 6}
```


## Using riskquant as a utility

```bash
bin/riskquant --file input.csv
```

The input.csv file should be formatted with columns

```less
Identifier,Name,Probability,Low_loss,High_loss
```
The columns are defined as follows:

* Identifier: An identifying label, which need not be unique, (see "Uniqueness of identifiers" below) but is 
  intended to provide a way of identifying the scenario. 
* Name: The name of the scenario, which should be more descriptive than the identifier.
* Probability: The chance that the loss will occur over some interval of time (typically a year). More
  precisely, this is defined as a rate of ocurrence (e.g. 0.1 means 1 occurrence per 10 years on average).
* Low_loss: The best-case scenario, given that the loss did occur. All our detection systems worked, so we
  found out about the event and remediated quickly.
* High_loss: The worst-cases scenario. Our detection systems didn't work, and the problem persisted for a long
  time until it was unavoidable to notice it and stop it.

The range [Low_loss, High_loss] should cover the 90% "confidence interval" of losses, i.e. we are 90% confident
that the loss would fall in that range. Given this range, we map to a Lognormal distribution, which allows for
no negative loss values, and for a long tail of high losses (allowing for blowout losses to occur that exceed the
"worst case" scenario.

Also, the Probability is mapped to a Poisson function so that the loss could actually occur more than once a
year, but on average occurs at the rate given.

For example:

```
ALICE,"Alice steals the data",0.01,1000000,10000000
BOB,"Bob steals the data",0.10,10000000,1000000000
CHARLIE,"Charlie loses the data",0.05,5000000,50000000
```

When run as an executable, the CSV input is converted to a CSV with a prioritized list of
loss scenarios:

```
BOB,Bob steals the data,"$26,600,000"
CHARLIE,Charlie loses the data,"$1,010,000"
ALICE,Alice steals the data,"$40,400"
```

Note that by default the output uses 3 significant digits, which is generally more than enough to capture
the precision of the inputs.

By default, the executable will also generate a Loss Exceedance Curve (LEC) which is a statistical 
description of the combined risk due to all the loss scenarios. The curve is generated by simulating
many possible years and summing the losses across all losses that occurred in that simulated year.
We then ask: "What loss magnitude was exceeded in 90% of the simulated years", 80%, 70% and so on.
The curve therefore shows the chance (y-axis) of exceeding some particular loss amount (x-axis) in aggregate across
all the scenarios.

### Command line arguments

Required argument:

```
--file : CSV of scenario name and parameters
```
  
Optional argument:

```
-V / --version : Version number
--years <n> : number of years to simulate' [ default 100,000 ]
--sigdigs <n> : number of significant digits in output values [ default 3 ]
--plot : Generate Loss Exceedance Curve [ default true ]
```


### Uniqueness of identifiers

An identifier could be duplicated, for example, if we distinguish between an internal
actor and an external attacker as variants of the same loss scenario, but with different (and
independent) probabilities and impacts.

## help(riskquant)

```less
Help on package riskquant:

NAME
   riskquant - Risk quantification library. Import models in this package as needed.

PACKAGE CONTENTS
   multiloss
   simpleloss

FUNCTIONS
   csv_to_simpleloss(file)
       Convert a csv file with parameters to SimpleModel objects

       :arg: file = Name of CSV file to read. Each row should contain rows with
                    name, probability, low_loss, high_loss

       :returns: List of SimpleLoss objects

   main(args=None)

DATA
   NAME_VERSION = 'riskquant 1.0'
   __appname__ = 'riskquant'

VERSION
   1.0
```

## help(riskquant.simpleloss)
```less
    |
    |  __init__(self, label, name, p, low_loss, high_loss)
    |      Initialize self.  See help(type(self)) for accurate signature.
    |
    |  annualized_loss(self)
    |      Expected mean loss per year as scaled by the probability of occurrence
    |
    |      :returns: Scalar of expected mean loss on an annualized basis.
    |
    |  simulate_losses_one_year(self)
    |      Generate a random number of losses, and loss amount for each.
    |
    |      :returns: List of loss amounts, or empty list if no loss occurred.
    |
    |  simulate_years(self, n)
    |      Draw randomly to simulate n years of possible losses.
    |
    |      :arg: n = Number of years to simulate
    |      :returns: List of length n with loss amounts per year. Amount is 0 if no loss occurred.
    |
    |  single_loss(self)
    |      Draw a single loss amount. Not scaled by probability of occurrence.
    |
    |      :returns: Scalar value of a randomly generated single loss amount.
    |
    |  ----------------------------------------------------------------------
    |  Data descriptors defined here:
    |
    |  __dict__
    |      dictionary for instance variables (if defined)
    |
    |  __weakref__
    |      list of weak references to the object (if defined)

DATA
   lognorm = <scipy.stats._continuous_distns.lognorm_gen object>
   norm = <scipy.stats._continuous_distns.norm_gen object>
```

## help(riskquant.multiloss)

```less
    |  Methods defined here:
    |
    |  __init__(self, loss_list)
    |      Initialize self.  See help(type(self)) for accurate signature.
    |
    |  loss_exceedance_curve(self, n, title='Aggregated Loss Exceedance', xlim=[1000000, 10000000000], savefile=None)
    |      Generate the Loss Exceedance Curve for the list of losses. (Uses simulate_years)
    |
    |      :arg: n = Number of years to simulate and display the LEC for.
    |            [title] = An alternative title for the plot.
    |            [xlim] = An alternative lower and upper limit for the plot's x axis.
    |            [savefile] = Save a PNG version to this file location instead of displaying.
    |
    |      :returns: None. If display=False, returns the matplotlib axis array
    |                (for customization).
    |
    |  prioritized_losses(self)
    |      Generate a prioritized list of losses from the loss list.
    |
    |      :returns: List of [(name, annualized_loss), ...] in descending order of annualized_loss.
    |
    |  simulate_years(self, n)
    |      Simulate n years across all the losses in the list.
    |
    |      :arg: n = The number of years to simulate
    |
    |      :returns: List of [loss_year_1, loss_year_2, ...] where each is a sum of all
    |                losses experienced that year.
    |
    |  ----------------------------------------------------------------------
    |  Data descriptors defined here:
    |
    |  __dict__
    |      dictionary for instance variables (if defined)
    |
    |  __weakref__
    |      list of weak references to the object (if defined)
```

