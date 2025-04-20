CREATE TABLE public.room (
	room_id uuid DEFAULT uuid_generate_v4() NOT NULL,
	start_time timestamp NOT NULL,
	end_time timestamp NULL,
	status varchar(20) DEFAULT 'ongoing'::character varying NULL,
	channel varchar(100) NULL,
	phone_number varchar(20) NULL,
	customer_id uuid NOT NULL,
	CONSTRAINT room_pkey PRIMARY KEY (room_id),
	CONSTRAINT fk_room_customer FOREIGN KEY (customer_id) REFERENCES public.customers(id)
);


CREATE TABLE public.customers (
	phone_number varchar NULL,
	channel varchar NULL,
	id uuid DEFAULT uuid_generate_v4() NOT NULL,
	CONSTRAINT customers_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_customers_phone_number ON public.customers USING btree (phone_number);


CREATE TABLE public.funnel (
	lead_id uuid DEFAULT uuid_generate_v4() NOT NULL,
	room_id uuid NULL,
	lead_date date NOT NULL,
	channel varchar(100) NULL,
	phone_number varchar(20) NULL,
	booking_date date NULL,
	transaction_date date NULL,
	transaction_value numeric(12, 2) NULL,
	CONSTRAINT funnel_pkey PRIMARY KEY (lead_id),
	CONSTRAINT funnel_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(room_id) ON DELETE SET NULL
);


CREATE TABLE public.message (
	message_id uuid NOT NULL,
	room_id uuid NOT NULL,
	sender_type varchar(20) NOT NULL,
	contents text NOT NULL,
	"timestamp" timestamp NOT NULL,
	channel varchar(100) NULL,
	phone_number varchar(20) NULL,
	CONSTRAINT message_pkey PRIMARY KEY (message_id),
	CONSTRAINT message_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(room_id) ON DELETE CASCADE
);