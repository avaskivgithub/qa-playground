using System;

namespace AbstractFactory
{
    class Program
    {
        static void Main(string[] args)
        {
            
            // 1. Select coffee mode
            // 2. Select extras if any
            // 3. Load everything
            // 4. Make and pour

            Console.WriteLine("\nMaking Coffee:");
            FactoryAbstractProduct coffeeMode = new FactoryCoffee();
            Customization extras = new Customization(){milk = 15, sugar = 25};
            VendingMachineSession vendingMachineSession = new VendingMachineSession(coffeeMode, extras);
            vendingMachineSession.GetDrinkReady();

            Console.WriteLine("\nMaking TEA:");
            FactoryAbstractProduct teaMode = new FactoryTea();
            Customization extras2 = new Customization(){milk = 15, sugar = 0};
            VendingMachineSession vendingMachineSession2 = new VendingMachineSession(teaMode, extras2);
            vendingMachineSession2.GetDrinkReady();
        }
    }

    /// <summary>
    /// The 'Client' class. Interaction environment for the products.
    /// uses only interfaces declared by AbstractFactory and AbstractProduct classes.
    /// </summary>
    class VendingMachineSession
    {
        private ProductAbstractBase _drink;
    
        // Constructor
        public VendingMachineSession(FactoryAbstractProduct factory, Customization cust)
        {
            _drink = factory.GetProduct(cust);
        }
    
        public void GetDrinkReady()
        {
        //_abstractProductB.Interact(_abstractProductA);
        _drink.Make();
        Console.WriteLine($"Pouring {_drink.GetType().Name}");
        }
    }
    public abstract class FactoryAbstractProduct
    {
        public abstract ProductAbstractBase GetProduct(Customization cust);
    }

    public class FactoryCoffee : FactoryAbstractProduct
    {
        public override ProductAbstractBase GetProduct(Customization cust)
        {
            return new ProductCoffee(cust);
        }
    }

    public class FactoryTea : FactoryAbstractProduct
    {
        public override ProductAbstractBase GetProduct(Customization cust)
        {
            return new ProductTea(cust);
        }
    }

    public abstract class ProductAbstractBase
    {
        public Customization customization;

        public ProductAbstractBase(Customization cust)
        {
            this.customization = cust;
        }

        public abstract void Make();

        public void AddSugar()
        {
            Console.WriteLine($"Add sugar: {customization.sugar}");
        }

        public void AddMilk()
        {
            Console.WriteLine($"Add milk: {customization.milk}");
        }

    }
    public class ProductCoffee : ProductAbstractBase
    {
        public Preparation preparation;

        public ProductCoffee(Customization cust) : base(cust)
        {
            this.preparation = new Preparation()
            {
                water = 250,
                coffee = 25,
                sugar = 0,
                milk = 0
            };
        }

        public override void Make()
        {
            Console.WriteLine($"{this.GetType().Name} coffee={this.preparation.coffee}, water={this.preparation.water} with sugar={this.preparation.sugar} and milk={this.preparation.milk}");
            this.AddSugar();
            this.AddMilk();
        }

        public new void AddSugar()
        {
            Console.WriteLine($"Add sugar: {customization.sugar} modified {this.GetType().Name}");
        }
    }

    public class ProductTea : ProductAbstractBase
    {
        public Preparation preparation;

        public ProductTea(Customization cust) : base(cust)
        {
            this.preparation = new Preparation()
            {
                water = 250,
                tea = 25,
                sugar = 0,
                milk = 0
            };
        }

        public override void Make()
        {
            Console.WriteLine($"{this.GetType().Name} tea={this.preparation.coffee}, water={this.preparation.water} with sugar={this.preparation.sugar} and milk={this.preparation.milk}");
            this.AddSugar();
            this.AddMilk();
        } 
    }

    public class Preparation
    {
        public double water;
        public double tea;
        public double coffee;
        public double milk;
        public double sugar;
    }

    public class Customization
    {
        public double milk;
        public double sugar;
    }
}
