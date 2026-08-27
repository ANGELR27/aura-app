-- ============================================
-- AURA - Schema de Base de Datos Supabase (v4.0 Biblia & Social)
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- ============================================

-- 1. Tabla de Perfiles
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  avatar_url TEXT DEFAULT '',
  password TEXT NOT NULL DEFAULT '123456',
  status_phrase TEXT DEFAULT '✨ Viviendo un día a la vez',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Tabla de Publicaciones (Fotos, Textos, Notas de Voz)
CREATE TABLE IF NOT EXISTS posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  text TEXT,
  photo_url TEXT,
  audio_url TEXT,
  reactions JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS audio_url TEXT;

-- 3. Tabla de Comentarios
CREATE TABLE IF NOT EXISTS comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  text TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 4. Tabla de Hábitos / Metas
CREATE TABLE IF NOT EXISTS habits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  text TEXT NOT NULL,
  is_done BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. Tabla de Historias / Momentos (24h)
CREATE TABLE IF NOT EXISTS stories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  photo_url TEXT NOT NULL,
  caption TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 6. Tabla de Notas Bíblicas & Subrayados Compartidos
CREATE TABLE IF NOT EXISTS bible_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  book_id INT NOT NULL,
  chapter INT NOT NULL,
  verse INT NOT NULL,
  highlight_color TEXT,
  note_text TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE habits ENABLE ROW LEVEL SECURITY;
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE bible_notes ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'public_profiles') THEN
    CREATE POLICY "public_profiles" ON profiles FOR ALL USING (true) WITH CHECK (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'public_posts') THEN
    CREATE POLICY "public_posts" ON posts FOR ALL USING (true) WITH CHECK (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'public_comments') THEN
    CREATE POLICY "public_comments" ON comments FOR ALL USING (true) WITH CHECK (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'public_habits') THEN
    CREATE POLICY "public_habits" ON habits FOR ALL USING (true) WITH CHECK (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'public_stories') THEN
    CREATE POLICY "public_stories" ON stories FOR ALL USING (true) WITH CHECK (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'public_bible_notes') THEN
    CREATE POLICY "public_bible_notes" ON bible_notes FOR ALL USING (true) WITH CHECK (true);
  END IF;
END $$;

-- Storage Bucket para Fotos y Audios
INSERT INTO storage.buckets (id, name, public) VALUES ('photos', 'photos', true)
ON CONFLICT (id) DO NOTHING;

DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'photos_select') THEN
    CREATE POLICY "photos_select" ON storage.objects FOR SELECT USING (bucket_id = 'photos');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'photos_insert') THEN
    CREATE POLICY "photos_insert" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'photos');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'photos_update') THEN
    CREATE POLICY "photos_update" ON storage.objects FOR UPDATE USING (bucket_id = 'photos');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'photos_delete') THEN
    CREATE POLICY "photos_delete" ON storage.objects FOR DELETE USING (bucket_id = 'photos');
  END IF;
END $$;

-- Perfiles iniciales de Roxana y Ángel
INSERT INTO profiles (id, email, name, avatar_url, password) VALUES
  ('a1000000-0000-0000-0000-000000000001', 'roxana@aura.app', 'Roxana', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80', 'roxana123'),
  ('a1000000-0000-0000-0000-000000000002', 'angel@aura.app', 'Ángel', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80', 'angel123')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name, avatar_url = EXCLUDED.avatar_url;

-- Habilitar sincronización en tiempo real
ALTER PUBLICATION supabase_realtime ADD TABLE posts;
ALTER PUBLICATION supabase_realtime ADD TABLE comments;
ALTER PUBLICATION supabase_realtime ADD TABLE habits;
ALTER PUBLICATION supabase_realtime ADD TABLE stories;
ALTER PUBLICATION supabase_realtime ADD TABLE bible_notes;
