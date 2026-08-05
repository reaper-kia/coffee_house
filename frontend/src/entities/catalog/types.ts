export interface MenuCategory {
  id: string;
  title: string;
  position: number;
  is_active: boolean;
}

export interface MenuItem {
  id: string;
  category_id: string | null;
  category_title: string | null;
  title: string;
  description: string | null;
  price_amount: string | number;
  price_currency: string;
  image_url: string | null;
  is_available: boolean;
  position: number;
}
