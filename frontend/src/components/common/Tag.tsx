import type { Tag as TagType } from '../../types'

interface TagProps {
  tag: TagType
}

export function Tag({ tag }: TagProps) {
  return (
    <span className={`tag ${tag.type}`}>
      {tag.label}
    </span>
  )
}

interface TagsProps {
  tags: TagType[]
}

export function Tags({ tags }: TagsProps) {
  if (!tags || tags.length === 0) return null

  return (
    <div className="tags">
      {tags.map((tag, index) => (
        <Tag key={`${tag.label}-${index}`} tag={tag} />
      ))}
    </div>
  )
}
