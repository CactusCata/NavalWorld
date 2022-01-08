// ---===== Exemple 1 =====--- Le main

public static void main(String[] args) {

}

// ---===== Exemple 2 =====--- Variables globales

public static int STATE = 1;

// ---===== Exemple 3 =====--- Classe et instanciation

public class Car {

  public Car(String carName, String carColor) {
    this.carName = carName;
    this.setCarColor(carColor);
  }

  public String getCarColor() {
    return this.carColor;
  }

  public void setCarColor(String carColor) {
    this.carColor = carColor;
  }

}

public class Main {

  public static void main(String[] args) {
    Car someCar = new Car("Hyundai", "Black");
    System.out.println(someCar.getCarColor());
    someCar.setCarColor("Blue");
  }

}

// ---===== Exemple 4 =====--- Maps

Map<K, V> map = new HashMap<>();

// ---===== Exemple 5 =====--- String format

int a = 5;
int b = 12;
System.out.println(a + " + " + b + " = " + (a + b));
