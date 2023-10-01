# Introduction

There are many different ways that Munki can be used.  Let's outline a few of these setups.

## Apple Updates Only

If you do not want to setup the infrastructure for a full blown Munki setup, you can have Munki install only Apple Software Updates.  This is helpful because this allows users without administrative rights the ability to install Apple updates.  See [[Apple Software Updates With Munki]] for details.

## Integrate with Existing Environment

If you currently use a monolithic or modular image to build your machines, you can use Munki to update the software on machines after they've been deployed. This requires a Munki repository plus installing and configuring the Munki tools on each client machine. This method can be put into place on top of any environment that isn't currently managed by any other means.  An example of this workflow would be as follows:

**New or Reimaged Machines**
- Apply Image
- Munki Pushes updates to machines as you add them

**Existing Machines**
- Install and configure Munki
- Munki ensures software is up to date

### Benefits

- After Imaging,  machines are fully updated by munki
- Less work up front

### Drawbacks

- Packages are managed in multiple places
- Duplication of effort with multiple images
- Not as agile when new machines are released
- More prone to human error

## Thin Imaging

Thin imaging is when you take a minimal base image (For example, 10.7 with only Apple Software Updates applied) or no image at all (Install software on top of new machines as they come from Apple).  This method uses the functionality found here: [[Bootstrapping With Munki]]

Example Workflow:

**New Machine**
- Apply Munki Client + Configuration
- Boot Machine and Munki installs software

**Reimage Machine**
- Apply Base Image
- Apply Munki Client + Configuration
- Boot Machine and Munki installs software

**Existing Machines**
- Install Munki Client + Configuration
- Munki ensures software is up to date

### Benefits

- Packages are managed in only one place
- After "Imaging," machines are fully updated
- Extremely agile when new machines are released
- Reusable for future configurations
- Little work duplication

### Drawbacks

- Takes slightly longer to complete
- More work up front